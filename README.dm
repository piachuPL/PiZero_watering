# Hello
That is my first app on GitHub

Its Python script for Raspberry in my case Raspberry Pi Zero W it's a brain for watering system.

PiZeroW had a rain sensor attached and release turn ON/OFF valves for watering at setting time

MQTT infos are sending to my Home Assistan mqtt brocker. My hassio confing file:

configuration.yaml

switch:    
  - platform: mqtt
    name: "Deszcz na Spalonej"
    state_topic: "stat/spalona/rain_sensor"
    command_topic: "cmnd/spalona/rain_sensor"
    payload_on: "ON"
    payload_off: "OFF"
    optimistic: false
    qos: 1
    retain: true
    
  - platform: mqtt
    name: "Zawor 1"
    state_topic: "stat/spalona/zawor1"
    command_topic: "cmnd/spalona/zawor1"
    payload_on: "ON"
    payload_off: "OFF"
    optimistic: false
    qos: 1
    retain: true

  - platform: mqtt
    name: "Zawor 2"
    state_topic: "stat/spalona/zawor2"
    command_topic: "cmnd/spalona/zawor2"
    payload_on: "ON"
    payload_off: "OFF"
    optimistic: false
    qos: 1
    retain: true
    
  - platform: mqtt
    name: "Zawor 3"
    state_topic: "stat/spalona/zawor3"
    command_topic: "cmnd/spalona/zawor3"
    payload_on: "ON"
    payload_off: "OFF"
    optimistic: false
    qos: 1
    retain: true
    