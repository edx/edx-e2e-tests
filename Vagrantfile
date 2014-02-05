# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$script = <<SCRIPT


    # Install system requirements
    apt-get update -y
    apt-get install -y git python2.7 python-pip python2.7-dev firefox dbus-x11 vim
    pip install virtualenv==1.10.1
    pip install virtualenvwrapper

    # Create a login script to create the virtualenv
    cat > /home/vagrant/.bash_profile <<INIT
export WORKON_HOME=/home/vagrant/.virtualenvs
mkdir -p /home/vagrant/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
source /home/vagrant/.virtualenvs/e2e/bin/activate
INIT

    # Install Python requirements and page objects
    sudo -u vagrant virtualenv /home/vagrant/.virtualenvs/e2e
    sudo -u vagrant PYTHONUNBUFFERED=1 sh -c ". /home/vagrant/.virtualenvs/e2e/bin/activate && pip install -r /home/vagrant/edx-e2e-tests/requirements/base.txt && fab -f /home/vagrant/edx-e2e-tests/fabfile.py install_pages"

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.33.10"

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
