from e2e_framework.page_object import PageObject


class OpenResponsePage(PageObject):
    """
    Open-ended response in the courseware.
    """

    @property
    def name(self):
        return "lms.open_response"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        """
        Open-response isn't associated with a particular URL.
        """
        raise NotImplemented

    def is_browser_on_page(self):
        return self.is_css_present('section.xmodule_CombinedOpenEndedModule')

    @property
    def assessment_type(self):
        """
        Return the type of assessment currently active.
        Options are:
            * "self"
            * "ai"
            * "peer"
        """
        label = self.css_text('section#combined-open-ended-status>div.statusitem-current')

        # Provide some tolerance to UI changes
        label_compare = label.lower().strip()

        if 'self' in label_compare:
            return 'self'
        elif 'ai' in label_compare:
            return 'ai'
        elif 'peer' in label_compare:
            return 'peer'
        else:
            raise ValueError("Unexpected assessment type: '{0}'".format(label))

    @property
    def prompt(self):
        """
        Return an HTML string representing the essay prompt.
        """
        prompt_css = "section.open-ended-child>div.prompt"
        elements = self.css_find(prompt_css)

        if len(elements) == 0:
            self.warning("Could not find essay prompt on page.")
            return ""

        elif len(elements) > 1:
            self.warning("Multiple essay prompts found on page; using the first one.")

        return elements.first.html.strip()

    @property
    def has_rubric(self):
        """
        Return a boolean indicating whether the rubric is available.
        """
        return self.is_css_present('div.rubric')

    @property
    def rubric_categories(self):
        """
        Return a list of categories available in the essay rubric.

        Example:
            ["Writing Applications", "Language Conventions"]

        The rubric is not always visible; if it's not available,
        this will return an empty list.
        """
        return [el.text for el in self.css_find('span.rubric-category')]

    @property
    def rubric_feedback(self):
        """
        Return a list of correct/incorrect feedback for each rubric category (e.g. from self-assessment).
        Example: ['correct', 'incorrect']

        If no feedback is available, returns an empty list.
        If feedback could not be interpreted (unexpected CSS class),
            the list will contain a `None` item.
        """

        # Get the green checkmark / red x labels
        # We need to filter out the similar-looking CSS classes
        # for the rubric items that are NOT marked correct/incorrect
        feedback_css = 'div.rubric-label>label'
        labels = [
            el['class'] for el in self.css_find(feedback_css)
            if el['class'] != 'rubric-elements-info'
        ]

        # Map CSS classes on the labels to correct/incorrect
        def map_feedback(css_class):
            if 'choicegroup_incorrect' in css_class:
                return 'incorrect'
            elif 'choicegroup_correct' in css_class:
                return 'correct'
            else:
                return None

        return map(map_feedback, labels)

    @property
    def alert_message(self):
        """
        Alert message displayed to the user.
        """
        alert_css = "div.open-ended-alert"
        return self.css_text(alert_css)

    @property
    def grader_status(self):
        """
        Status message from the grader.
        If not present, return an empty string.
        """
        return self.css_text('div.grader-status')

    def set_response(self, response_str):
        """
        Input a response to the prompt.
        """
        input_css = "textarea.short-form-response"
        self.css_fill(input_css, response_str)

    def save_response(self):
        """
        Save the response for later submission.
        """
        self.css_click('input.save-button')

    def submit_response(self):
        """
        Submit a response for grading.
        """
        self.css_click('input.submit-button')

        # Dismiss the alert that pops up
        self.browser.get_alert().accept()

    def submit_self_assessment(self, scores):
        """
        Submit a self-assessment rubric.
        `scores` is a list of scores (0 to max score) for each category in the rubric.
        """

        # Warn if we have the wrong number of scores
        num_categories = len(self.rubric_categories)
        if len(scores) != num_categories:
            msg = "Recieved {0} scores but there are {1} rubric categories".format(
                len(scores), num_categories
            )
            self.warning(msg)

        # Set the score for each category
        for score_index in range(len(scores)):

            # Convert the list index (starts at 0) to CSS index (starts at 1)
            input_css = "div.rubric>ul.rubric-list:nth-of-type({0}) input.score-selection".format(score_index + 1)
            inputs = self.css_find(input_css)

            score_num = scores[score_index]
            if score_num >= len(inputs):
                msg = "Tried to select score {0} but there are only {1} options".format(score_num, len(inputs))
                self.warning(msg)

            else:
                inputs[score_num].check()

        # Wait for the button to become enabled
        button_css = 'input.submit-button'
        button = self.css_find(button_css).first
        self.wait_for(lambda _: not button['disabled'])

        # Submit the assessment
        self.css_click('input.submit-button')
