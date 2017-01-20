# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$script = <<SCRIPT


    # Install system requirements
    apt-get update -y
    apt-get install -y git python2.7 python-pip python2.7-dev firefox dbus-x11 vim libjpeg-dev libxml2-dev libxslt1-dev
    apt-get install -y libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
    pip install virtualenv==1.10.1
    pip install virtualenvwrapper

    # Create a login script to create the virtualenv
    cat > /home/vagrant/.bash_profile <<INIT
export WORKON_HOME=/home/vagrant/.virtualenvs
mkdir -p /home/vagrant/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
source /home/vagrant/.virtualenvs/e2e/bin/activate
INIT

    # Install Python requirements
    sudo -u vagrant virtualenv /home/vagrant/.virtualenvs/e2e
    sudo -u vagrant PYTHONUNBUFFERED=1 sh -c ". /home/vagrant/.virtualenvs/e2e/bin/activate && STATIC_DEPS=true CFLAGS="-O0 -fPIC"  pip install "lxml==3.4.4" && pip install -r /home/vagrant/edx-e2e-tests/requirements/base.txt"

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/home/vagrant/edx-e2e-tests"

  # Provision the box
  config.vm.provision "shell", inline: $script

  # X11 forwarding
  config.ssh.forward_x11 = true

end
