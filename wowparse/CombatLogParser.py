import csv
import logging

from Event import Event

class CombatLogParser(object):
    def __init__(self):
        self.__logger = logging.getLogger("wowparse.CombatLogParser")

    def parse(self, filename, progress_callback):
        progress_callback(0)
        rows = self.__parse_file(filename)
        progress_callback(20)

        # TODO: put this into a state object
        event_count = len(rows)
        events = {}
        unknown_events = []

        id = 0
        for row in rows:
            if len(row) >= 9:
                scratch = row[0].split("  ")
                event = Event(id, scratch[0], scratch[1], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9:])
                if event.unknown:
                    unknown_events.append(event)
                events[id] = event
            else:
                self.__logger.warning("Invalid event found!")

            # TODO: this math seems wrong (why 0.25 and not .20???), double check it
            progress = id / (event_count + (0.25 * event_count))
            progress_callback(20 + int(progress * 100.0))
            id += 1

        progress_callback(100)

        self.__logger.info("Found %d unknown events" % len(unknown_events))
        for event in unknown_events:
            self.__logger.debug("Unknown event: %s" % event)

        return events

    def __parse_file(self, filename):
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                return [ row for row in reader]
        except IOError, e:
            self.__logger.warning("Unable to open '%s': %s" % (filename, e))
        return []
