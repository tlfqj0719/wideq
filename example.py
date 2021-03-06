import wideq
import json
import time
import argparse
import sys
import os
import datetime

STATE_FILE = 'wideq_state.json'
DEBUG_MODE = False

def authenticate(gateway):
    """Interactively authenticate the user via a browser to get an OAuth
    session.
    """

    login_url = gateway.oauth_url()
    print('Log in here:')
    print(login_url)
    print('Then paste the URL where the browser is redirected:')
    callback_url = input()
    return wideq.Auth.from_url(gateway, callback_url)


def ls(client):
    """List the user's devices."""

    for device in client.devices:
        print('{0.id}: {0.name} ({0.type.name} {0.model_id})'.format(device))


def mon(client, device_id):
    """Monitor any device, displaying generic information about its
    status.
    """

    device = client.get_device(device_id)
    model = client.model_info(device)
    device.load_model_info
    device.load_lang_pack_product
    device.load_lang_pack_model

    with wideq.Monitor(client.session, device_id) as mon:
        try:
            while True:
                time.sleep(1)
                now = datetime.datetime.now()
                print('polling... {}:{}:{}'.format(now.hour, now.minute, now.second))
                data = mon.poll()
                if data:
                    try:
                        res = model.decode_monitor(data)
                        if DEBUG_MODE:
                            with open(device.name + '_polling.json', 'w', -1, 'utf-8') as outfile:
                                json.dump(res, outfile, ensure_ascii=False, indent="\t")
                    except ValueError:
                        print('status data: {!r}'.format(data))
                    else:
                        for key, value in res.items():
                            try:
                                desc = model.value(key)
                            except KeyError:
                                print('- {}: {}'.format(key, value))
                            if isinstance(desc, wideq.EnumValue):
                                print('- {}: {}'.format(
                                    key, desc.options.get(value, value)
                                ))
                            elif isinstance(desc, wideq.RangeValue):
                                print('- {0}: {1} ({2.min}-{2.max})'.format(
                                    key, value, desc,
                                ))

        except KeyboardInterrupt:
            pass

def dehum_mon(client, device_id):
    device = client.get_device(device_id)
    if device.type != wideq.DeviceType.DEHUMIDIFIER:
        print('This is not an DEHUMIDIFIER device.')
        return

    machine = wideq.DehumDevice(client, device)

    try:
        machine.monitor_start()
        while True:
            time.sleep(1)
            state = machine.poll()
            if state:
                now = datetime.datetime.now()
                print('polling... {}:{}:{}'.format(now.hour, now.minute, now.second))
                print('device_name: ', state.device_name)
                print('is_on: ', state.is_on)
                print('device_type: ', state.device_type)
                print('state: ', state.state)
                print('mode: ', state.mode)
                print('windstrength_state: ', state.windstrength_state)
                print('airremoval_state: ', state.airremoval_state)
                print('current_humidity: ', state.current_humidity)
                print('target_humidity: ', state.target_humidity)
                if DEBUG_MODE:
                    with open(device.name + '_polling.json', 'w', -1, 'utf-8') as outfile:
                        json.dump(state.data, outfile, ensure_ascii=False, indent="\t")
    except KeyboardInterrupt:
        pass
    finally:
        machine.monitor_stop()

def washer_mon(client, device_id):
    device = client.get_device(device_id)
    if device.type != wideq.DeviceType.WASHER:
        print('This is not an WASHER device.')
        return

    machine = wideq.WasherDevice(client, device)

    try:
        machine.monitor_start()
        while True:
            time.sleep(1)
            state = machine.poll()
            if state:
                now = datetime.datetime.now()
                print('polling... {}:{}:{}'.format(now.hour, now.minute, now.second))
                print('device_name: ', state.device_name)
                print('is_on: ', state.is_on)
                print('device_type: ', state.device_type)
                print('state: ', state.state)
                print('remaining_time: ', state.remaining_time)
                print('initial_time: ', state.initial_time)
                print('reserve_time: ', state.reserve_time)
                print('previous_state: ', state.previous_state)
                print('smart_course: ', state.smart_course)
                print('course: ', state.course)
                print('error: ', state.error)
                print('soil_level: ', state.soil_level)
                print('water_temp: ', state.water_temp)
                print('spin_speed: ', state.spin_speed)
                print('rinse_count: ', state.rinse_count)
                print('dry_level: ', state.dry_level)
                print('water_level: ', state.water_level)
                print('water_flow: ', state.water_flow)
                print('soak: ', state.soak)
                print('fresh_care: ', state.fresh_care)
                print('child_lock: ', state.child_lock)
                print('door_lock: ', state.door_lock)
                print('steam: ', state.steam)
                print('turbo_shot: ', state.turbo_shot)
                print('buzzer: ', state.buzzer)
                print('sterilize: ', state.sterilize)
                print('heater: ', state.heater)
                print('tubclean_count: ', state.tubclean_count)
                print('load_level: ', state.load_level)
                if DEBUG_MODE:
                    with open(device.name + '_polling.json', 'w', -1, 'utf-8') as outfile:
                        json.dump(state.data, outfile, ensure_ascii=False, indent="\t")
    except KeyboardInterrupt:
        pass
    finally:
        machine.monitor_stop()

def dryer_mon(client, device_id):
    device = client.get_device(device_id)
    if device.type != wideq.DeviceType.DRYER:
        print('This is not an DRYER device.')
        return

    machine = wideq.DryerDevice(client, device)

    try:
        machine.monitor_start()
        while True:
            time.sleep(1)
            state = machine.poll()
            if state:
                now = datetime.datetime.now()
                print('polling... {}:{}:{}'.format(now.hour, now.minute, now.second))
                print('device_name: ', state.device_name)
                print('is_on: ', state.is_on)
                print('device_type: ', state.device_type)
                print('state: ', state.state)
                print('remaining_time: ', state.remaining_time)
                print('initial_time: ', state.initial_time)
                print('reserve_time: ', state.reserve_time)
                print('process_state: ', state.process_state)
                print('smart_course: ', state.smart_course)
                print('course: ', state.course)
                print('error: ', state.error)
                print('dry_level: ', state.dry_level)
                print('eco_hybrid: ', state.eco_hybrid)
                print('anti_crease: ', state.anti_crease)
                print('child_lock: ', state.child_lock)
                print('self_cleaning: ', state.self_cleaning)
                print('damp_dry_beep: ', state.damp_dry_beep)
                print('hand_iron: ', state.hand_iron)
                if DEBUG_MODE:
                    with open(device.name + '_polling.json', 'w', -1, 'utf-8') as outfile:
                        json.dump(state.data, outfile, ensure_ascii=False, indent="\t")
    except KeyboardInterrupt:
        pass
    finally:
        machine.monitor_stop()

def ac_mon(client, device_id):
    """Monitor an AC/HVAC device, showing higher-level information about
    its status such as its temperature and operation mode.
    """

    device = client.get_device(device_id)
    if device.type != wideq.DeviceType.AC:
        print('This is not an AC device.')
        return

    ac = wideq.ACDevice(client, device)

    try:
        ac.monitor_start()
        while True:
            time.sleep(1)
            state = ac.poll()
            if state:
                print(
                    '{1}; '
                    '{0.mode.name}; '
                    'cur {0.temp_cur_f}°F; '
                    'cfg {0.temp_cfg_f}°F; '
                    'fan speed {0.fan_speed.name}'
                    .format(
                        state,
                        'on' if state.is_on else 'off'
                    )
                )

    except KeyboardInterrupt:
        pass
    finally:
        ac.monitor_stop()


class UserError(Exception):
    """A user-visible command-line error.
    """
    def __init__(self, msg):
        self.msg = msg


def _force_device(client, device_id):
    """Look up a device in the client (using `get_device`), but raise
    UserError if the device is not found.
    """
    device = client.get_device(device_id)
    if not device:
        raise UserError('device "{}" not found'.format(device_id))
    return device


def set_temp(client, device_id, temp):
    """Set the configured temperature for an AC device."""

    ac = wideq.ACDevice(client, _force_device(client, device_id))
    ac.set_fahrenheit(int(temp))


def turn(client, device_id, on_off):
    """Turn on/off an AC device."""

    ac = wideq.ACDevice(client, _force_device(client, device_id))
    ac.set_on(on_off == 'on')


def ac_config(client, device_id):
    ac = wideq.ACDevice(client, _force_device(client, device_id))
    print(ac.get_filter_state())
    print(ac.get_mfilter_state())
    print(ac.get_energy_target())
    print(ac.get_volume())
    print(ac.get_light())
    print(ac.get_zones())


EXAMPLE_COMMANDS = {
    'ls': ls,
    'mon': mon,
    'washer-mon': washer_mon,
    'dryer-mon': dryer_mon,
    'dehum-mon': dehum_mon,
    'ac-mon': ac_mon,
    'set-temp': set_temp,
    'turn': turn,
    'ac-config': ac_config,
}


def example_command(client, cmd, args):
    func = EXAMPLE_COMMANDS[cmd]
    func(client, *args)


def example(country, language, cmd, args):
    # Load the current state for the example.
    try:
        with open(STATE_FILE, 'r', -1, 'utf-8') as f:
            state = json.load(f)
    except IOError:
        state = {}

    client = wideq.Client.load(state)
    if country:
        client._country = country
    if language:
        client._language = language

    # Log in, if we don't already have an authentication.
    if not client._auth:
        client._auth = authenticate(client.gateway)

    # Loop to retry if session has expired.
    while True:
        try:
            example_command(client, cmd, args)
            break

        except wideq.NotLoggedInError:
            print('Session expired.')
            client.refresh()

        except UserError as exc:
            print(exc.msg, file=sys.stderr)
            sys.exit(1)

    # Save the updated state.
    state = client.dump()
    with open(STATE_FILE, 'w', -1, 'utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent="\t")


def main():
    """The main command-line entry point.
    """
    parser = argparse.ArgumentParser(
        description='Interact with the LG SmartThinQ API.'
    )
    parser.add_argument('cmd', metavar='CMD', nargs='?', default='ls',
                        help='one of {}'.format(', '.join(EXAMPLE_COMMANDS)))
    parser.add_argument('args', metavar='ARGS', nargs='*',
                        help='subcommand arguments')

    parser.add_argument(
        '--country', '-c',
        help='country code for account (default: {})'
        .format(wideq.DEFAULT_COUNTRY)
    )
    parser.add_argument(
        '--language', '-l',
        help='language code for the API (default: {})'
        .format(wideq.DEFAULT_LANGUAGE)
    )

    args = parser.parse_args()
    example(args.country, args.language, args.cmd, args.args)


if __name__ == '__main__':
    main()
