# moneypit-power-monitor

Used to monitor overall power usage for our crypto mine, which is supplied by 277 volt 3-phase that is transformed to 220V single phase (for miners) / 120V (for supporting devices).

Designed to run on a Raspberry Pi W (w/ RASPBIAN LITE v2.9) with the following sensors / controls:

- ADS1115 16-Bit ADC - 4 Channel with Programmable Gain Amplifier  (https://www.adafruit.com/product/1085?gclid=EAIaIQobChMIjoDv3_ak3gIVhrbACh0_vAzBEAYYAiABEgLh0vD_BwE)

- [QTY 3] YHDC SCT036TS-D Split Core Current Transformer Sensor Input 400A Output 5V Black (http://en.yhdc.com/product/SCT036TS-D-379.html)

Each current sensor is polled periodically (based upon config setting) and the values are stored in REDIS and available by a single API endpoint and simple UI for review of current state of power usage.

Power usage is also indexed in Elasticsearch (in batches based upon config setting).


## Dependencies
>
> Recommend  `sudo apt-get update` if fresh install

- I2C interface on Raspberry Pi must be enabled via `raspi-config` and install i2c tools
   `sudo apt-get install i2c-tools`

- Git
   `sudo apt-get install git`

- Python 2 w/ pip
  `sudo apt-get install python-pip`
  `sudo python -m pip install --upgrade pip setuptools wheel`

- Redis Server
   `sudo apt-get install redis-server`

- Npm / Node
   `sudo apt-get install npm`
   `sudo apt-get install nodejs`

- PHP CLI / Curl
   `sudo apt-get install php7.0-cli`
   `sudo apt-get install php7.0-curl`

- Python library for ADS1115 (recommend installing from source)
  `https://github.com/adafruit/Adafruit_Python_ADS1x15`

- Python library for Elasticsearch and Redis
  `sudo pip install elasticsearch`
  `sudo pip install redis`

- A remote `elasticsearch` to post stats to

## Install

- Clone repo `git clone https://github.com/moneypit/moneypit-power-monitor`

- Rename `config_sample.json` to `config.json`

- Update config

```



```

- Enable `redis-server` service is start on reboot

`sudo systemctl enable redis-server`


- Configure node / redis to start following reboot `/etc/rc.local`

```

	#!/bin/sh -e
	#
	# rc.local
	#
	# This script is executed at the end of each multiuser runlevel.
	# Make sure that the script will "exit 0" on success or any other
	# value on error.
	#
	# In order to enable or disable this script just change the execution
	# bits.
	#
	# By default this script does nothing.

	# Print the IP address
	_IP=$(hostname -I) || true
	if [ "$_IP" ]; then
	  printf "My IP address is %s\n" "$_IP"
	fi

	# Start moneypit-power-monitor node app / api
	sudo /usr/bin/npm start --cwd /home/pi/moneypit-power-monitor --prefix /home/pi/moneypit-power-monitor &

  sudo /usr/bin/python /home/pi/moneypit-power-monitor/scripts/fetch-power.py /home/pi/moneypit-power-monitor/config.json &

	exit 0

```

- From within the `./moneypit-fan-controller-folder` install PHP / Node dependencies

  ```
   $ wget https://raw.githubusercontent.com/composer/getcomposer.org/1b137f8bf6db3e79a38a5bc45324414a6b1f9df2/web/installer -O - -q | php -- --quiet
   $ php composer.phar install
   $ npm install
  ```

- Setup the following cron jobs:

```

```

- Reboot the device to start processes

```
sudo reboot
```

## UI

`http://[hostname]:3000/`

## APIs

`GET /` => Swagger docs

`GET /power` => Returns current power information
