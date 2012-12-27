# http://www.wowpedia.org/API_COMBAT_LOG_EVENT
# http://www.wowpedia.org/API_UnitGUID
# http://www.wowpedia.org/RaidFlag

import logging

EVENT_PREFIXES = [ "SWING", "RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING", "ENVIRONMENTAL" ]

EVENT_SUFFIXES = [ "DAMAGE", "MISSED", "HEAL", "ENERGIZE", "DRAIN", "LEECH", "INTERRUPT", "DISPEL", "DISPEL_FAILED",
    "STOLEN", "EXTRA_ATTACKS", "AURA_APPLIED", "AURA_REMOVED", "AURA_APPLIED_DOSE", "AURA_REMOVED_DOSE",
    "AURA_REFRESH", "AURA_BROKEN", "AURA_BROKEN_SPELL", "CAST_START", "CAST_SUCCESS", "CAST_FAILED", "INSTAKILL",
    "DURABILITY_DAMAGE", "DURABILITY_DAMAGE_ALL", "CREATE", "SUMMON", "RESURRECT" ]

SPECIAL_EVENTS = [ "DAMAGE_SHIELD", "DAMAGE_SPLIT", "DAMAGE_SHIELD_MISSED", "ENCHANT_APPLIED", "ENCHANT_REMOVED",
    "PARTY_KILL", "UNIT_DIED", "UNIT_DESTROYED" ]

UNIT_TYPES = {
    0: "Player",
    1: "Object",
    3: "NPC",
    4: "Pet",
    5: "Vehicle",
}

SPELL_SCHOOLS = {
    0: "None",
    1: "Physical",
    2: "Holy",
    3: "Holystrike",
    4: "Fire",
    5: "Flamestrike",
    6: "Holyfire",
    8: "Nature",
    9: "Stormstrike",
    10: "Holystorm",
    12: "Firestorm",
    16: "Frost",
    17: "Froststrike",
    18: "Holyfrost",
    20: "Frostfire",
    24: "Froststorm",
    28: "Elemental",
    32: "Shadow",
    33: "Shadowstrike",
    34: "Shadowlight (Twilight)",
    36: "Shadowflame",
    40: "Shadowstorm (Plague)",
    48: "Shadowfrost",
    64: "Arcane",
    65: "Spellstrike",
    66: "Divine",
    68: "Spellfire",
    72: "Spellstorm",
    80: "Spellfrost",
    96: "Spellshadow",
    124: "Chromatic",
    126: "Magic",
    127: "Chaos",
}

POWER_TYPES = {
    -2: "Health",
    0: "Mana",
    1: "Rage",
    2: "Focus",
    3: "Energy",
    4: "Pet Happiness",
    5: "Runes",
    6: "Runic Power",
    7: "Soul Shards",
    8: "Eclipse",
    9: "Holy Power",
}

class Event(object):
    EVENT_MAP = {}
    EVENT_NAME_MAP = {}
    PREFIX_MAP = {}
    SUFFIX_MAP = {}

    @classmethod
    def build_event_tables(cls):
        setattr(cls, "EVENT_UNKNOWN", 0)
        cls.EVENT_MAP["EVENT_UNKNOWN"] = 0
        cls.EVENT_NAME_MAP[0] = "UNKNOWN"

        id = 1
        for prefix in EVENT_PREFIXES:
            for suffix in EVENT_SUFFIXES:
                value = "EVENT_%s_%s" % (prefix, suffix)

                setattr(cls, value, id)
                cls.EVENT_MAP[value] = id
                cls.EVENT_NAME_MAP[id] = "%s_%s" % (prefix, suffix)
                cls.PREFIX_MAP[value] = prefix
                cls.SUFFIX_MAP[value] = suffix

                id += 1

        for event in SPECIAL_EVENTS:
            value = "EVENT_%s" % event

            setattr(cls, value, id)
            cls.EVENT_MAP[value] = id
            cls.EVENT_NAME_MAP[id] = event

            id += 1

        cls.PREFIX_MAP["EVENT_DAMAGE_SHIELD"] = "SPELL"
        cls.SUFFIX_MAP["EVENT_DAMAGE_SHIELD"] = "DAMAGE"

        cls.PREFIX_MAP["EVENT_DAMAGE_SPLIT"] = "SPELL"
        cls.SUFFIX_MAP["EVENT_DAMAGE_SPLIT"] = "DAMAGE"

        cls.PREFIX_MAP["EVENT_DAMAGE_SHIELD_MISSED"] = "SPELL"
        cls.SUFFIX_MAP["EVENT_DAMAGE_SHIELD_MISSED"] = "MISSED"

    @classmethod
    def event_name(cls, id):
        return cls.EVENT_NAME_MAP[id] if cls.EVENT_NAME_MAP.has_key(id) else "UNKNOWN"

    @classmethod
    def event_type(cls, event):
        return cls.EVENT_MAP["EVENT_%s" % event] if cls.EVENT_MAP.has_key("EVENT_%s" % event) else "0"

    @classmethod
    def prefix_map(cls, event):
        return cls.PREFIX_MAP["EVENT_%s" % event] if cls.PREFIX_MAP.has_key("EVENT_%s" % event) else ""

    @classmethod
    def suffix_map(cls, event):
        return cls.SUFFIX_MAP["EVENT_%s" % event] if cls.SUFFIX_MAP.has_key("EVENT_%s" % event) else ""

    @staticmethod
    def unit_type(guid):
        type = (int(guid[0:5], 0) & 0x07)
        if UNIT_TYPES.has_key(type):
            return UNIT_TYPES[type]
        print("Unknown unit type: %s" % type)
        return "Unknown"

    @staticmethod
    def spell_school_conv(school):
        ischool = int(school, 0)
        if SPELL_SCHOOLS.has_key(ischool):
            return SPELL_SCHOOLS[ischool]
        print("Unknown school: %s" % school)
        return school

    @staticmethod
    def power_type_conv(power):
        ipower = int(power, 0)
        if POWER_TYPES.has_key(ipower):
            return POWER_TYPES[ipower]
        print("Unknown power type: %s" % power)
        return power

    @staticmethod
    def boolean(v):
        return "Yes" if v == "1" else "No"

    def __init__(self, id, timestamp, event, sourceGUID, sourceName, sourceFlags, sourceRaidFlags, destGUID, destName, destFlags, destRaidFlags, arguments):
        self.__logger = logging.getLogger("wowparse.Event")

        self.__id = id
        self.__timestamp = timestamp
        self.__event = Event.event_type(event)
        self.__prefix = Event.prefix_map(event)
        self.__suffix = Event.suffix_map(event)
        self.__source = (sourceGUID, "" if sourceName == "nil" else sourceName, sourceFlags, sourceRaidFlags)
        self.__source_type = Event.unit_type(self.source_guid)
        self.__dest = (destGUID, "" if destName == "nil" else destName, destFlags, destRaidFlags)
        self.__dest_type = Event.unit_type(self.dest_guid)
        self.__arguments = arguments

        self.__build_arguments()
        if len(self.__arguments) > 0:
            self.__logger.warning("Event %s has remaining arguments: %s" % (self.type_name, self.__arguments))

    @property
    def unknown(self):
        return self.__event == 0

    @property
    def id(self):
        return self.__id

    @property
    def prefix(self):
        return self.__prefix

    @property
    def suffix(self):
        return self.__suffix

    ### THESE ARE GENERIC EVENT DETAILS ###
    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def type(self):
        return self.__event

    @property
    def type_name(self):
        return Event.event_name(self.__event)

    @property
    def source_guid(self):
        return self.__source[0]

    @property
    def source_type(self):
        return self.__source_type

    @property
    def source_name(self):
        return self.__source[1]

    @property
    def source_flags(self):
        return self.__source[2]

    @property
    def source_raid_flags(self):
        return self.__source[3]

    @property
    def dest_guid(self):
        return self.__dest[0]

    @property
    def dest_type(self):
        return self.__dest_type

    @property
    def dest_name(self):
        return self.__dest[1]

    @property
    def dest_flags(self):
        return self.__dest[2]

    @property
    def dest_raid_flags(self):
        return self.__dest[3]

    ### END GENERIC EVENT DETAILS ###

    ### THESE ARE ALL EVENT TYPE SPECIFIC ARGUMENTS ###

    @property
    def has_spell_id(self):
        return self.prefix in ["RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING"]

    @property
    def spell_id(self):
        return self.__spell_id

    @property
    def has_spell_name(self):
        return self.type_name in ["ENCHANT_APPLIED", "ENCHANT_REMOVED"] or self.prefix in ["RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING"]

    @property
    def spell_name(self):
        return self.__spell_name

    @property
    def has_spell_school(self):
        return self.prefix in ["RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING"]

    @property
    def spell_school(self):
        return self.__spell_school

    @property
    def has_item_id(self):
        return self.type_name in ["ENCHANT_APPLIED", "ENCHANT_REMOVED"]

    @property
    def item_id(self):
        return self.__item_id

    @property
    def has_item_name(self):
        return self.type_name in ["ENCHANT_APPLIED", "ENCHANT_REMOVED"]

    @property
    def item_name(self):
        return self.__item_name

    @property
    def has_environmental_type(self):
        return self.prefix == "ENVIRONMENTAL"

    @property
    def environmental_type(self):
        return self.__environmental_type

    @property
    def has_amount(self):
        return self.suffix in [ "DAMAGE", "MISSED", "HEAL", "ENERGIZE", "DRAIN", "LEECH", "EXTRA_ATTACKS", "AURA_APPLIED_DOSE", "AURA_REMOVED_DOSE" ]

    @property
    def amount(self):
        return self.__amount

    @property
    def has_overkill(self):
        return self.suffix == "DAMAGE"

    @property
    def overkill(self):
        return self.__overkill

    @property
    def has_school(self):
        return self.suffix == "DAMAGE"

    @property
    def school(self):
        return self.__school

    @property
    def has_resisted(self):
        return self.suffix == "DAMAGE"

    @property
    def resisted(self):
        return self.__resisted

    @property
    def has_blocked(self):
        return self.suffix == "DAMAGE"

    @property
    def blocked(self):
        return self.__blocked

    @property
    def has_absorbed(self):
        return self.suffix in [ "DAMAGE", "HEAL" ]

    @property
    def absorbed(self):
        return self.__absorbed

    @property
    def has_critical(self):
        return self.suffix in [ "DAMAGE", "HEAL" ]

    @property
    def critical(self):
        return self.__critical

    @property
    def has_glancing(self):
        return self.suffix == "DAMAGE"

    @property
    def glancing(self):
        return self.__glancing

    @property
    def has_crushing(self):
        return self.suffix == "DAMAGE"

    @property
    def crushing(self):
        return self.__crushing

    @property
    def has_overhealing(self):
        return self.suffix == "HEAL"

    @property
    def overhealing(self):
        return self.__overhealing

    @property
    def has_miss_type(self):
        return self.suffix == "MISSED"

    @property
    def miss_type(self):
        return self.__miss_type

    @property
    def has_power_type(self):
        return self.suffix in [ "ENERGIZE", "DRAIN", "LEECH" ]

    @property
    def power_type(self):
        return self.__power_type

    @property
    def has_extra_amount(self):
        self.suffix in ["DRAIN", "LEECH"]

    @property
    def extra_amount(self):
        return self.__extra_amount

    @property
    def has_extra_spell_id(self):
        return self.suffix in [ "INTERRUPT", "DISPEL_FAILED", "DISPEL", "STOLEN", "AURA_BROKEN_SPELL" ]

    @property
    def extra_spell_id(self):
        return self.__extra_spell_id

    @property
    def has_extra_spell_name(self):
        return self.suffix in [ "INTERRUPT", "DISPEL_FAILED", "DISPEL", "STOLEN", "AURA_BROKEN_SPELL" ]

    @property
    def extra_spell_name(self):
        return self.__extra_spell_name

    @property
    def has_extra_school(self):
        return self.suffix in [ "INTERRUPT", "DISPEL_FAILED", "DISPEL", "STOLEN", "AURA_BROKEN_SPELL" ]

    @property
    def extra_school(self):
        return self.__extra_school

    @property
    def has_aura_type(self):
        return self.suffix in [ "DISPEL", "STOLEN", "AURA_BROKEN_SPELL", "AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH", "AURA_BROKEN", "AURA_APPLIED_DOSE", "AURA_REMOVED_DOSE" ]

    @property
    def aura_type(self):
        return self.__aura_type

    @property
    def has_remaining(self):
        return self.suffix in ["AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH"]

    @property
    def remaining(self):
        return self.__remaining

    @property
    def has_unknown1(self):
        return self.suffix in ["AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH"]

    @property
    def unknown1(self):
        return self.__unknown1

    @property
    def has_unknown2(self):
        return self.suffix in ["AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH"]

    @property
    def unknown2(self):
        return self.__unknown2

    @property
    def aura_type(self):
        return self.__aura_type

    @property
    def has_failed_type(self):
        return self.suffix == "CAST_FAILED"

    @property
    def failed_type(self):
        return self.__failed_type

    ### END EVENT TYPE SPECIFIC ARGUMENTS ###

    def __getitem__(self, key):
        if key == 0:
            return self.id
        elif key == 1:
            return self.timestamp
        elif key == 2:
            return self.type_name
        elif key == 3:
            return self.source_name
        elif key == 4:
            return self.dest_name

        if key >= 0:
            self.__logger.warning("wtf key: %s" % key)
        return None

    def __str__(self):
        ret = "event id=%d type=%s, source=%s, dest=%s" % (self.id, self.type_name, self.source_name, self.dest_name)

        if self.type_name in ["ENCHANT_APPLIED", "ENCHANT_REMOVED"]:
            ret = ret + (", spell name=%s, item id=%s, item name=%s" % (self.spell_name, self.item_id, self.item_name))

        if not self.prefix and not self.suffix:
            return ret

        if self.prefix in ["RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING"]:
            ret = ret + (", spell id=%s, spell name=%s, spell school=%s" % (self.spell_id, self.spell_name, self.spell_school))
        elif self.prefix == "ENVIRONMENTAL":
            ret = ret + (", environmental type=%s" % self.environmental_type)

        if self.suffix == "DAMAGE":
            ret = ret + (", amount=%s, overkill=%s, school=%s, resisted=%s, blocked=%s, absorbed=%s, critical=%s, glancing=%s, crushing=%s" % (self.amount, self.overkill, self.school, self.resisted, self.blocked, self.absorbed, self.critical, self.glancing, self.crushing))
        elif self.suffix == "MISSED":
            ret = ret + (", type=%s, amount=%s" % (self.miss_type, self.amount))
        elif self.suffix == "HEAL":
            ret = ret + (", amount=%s, overhealing=%s, absorbed=%s, critical=%s" % (self.amount, self.overhealing, self.absorbed, self.critical))
        elif self.suffix == "ENERGIZE":
            ret = ret + (", amount=%s, power type=%s" % (self.amount, self.power_type))
        elif self.suffix in ["DRAIN", "LEECH"]:
            ret = ret + (", amount=%s, power type=%s, extra amount=%s" % (self.amount, self.power_type, self.extra_amount))
        elif self.suffix in ["INTERRUPT", "DISPEL_FAILED"]:
            ret = ret + (", extra spell id=%s, extra spell name=%s, extra school=%s" % (self.extra_spell_id, self.extra_spell_name, self.extra_school))
        elif self.suffix in ["DISPEL", "STOLEN", "AURA_BROKEN_SPELL"]:
            ret = ret + (", extra spell id=%s, extra spell name=%s, extra school=%s, aura type=%s" % (self.extra_spell_id, self.extra_spell_name, self.extra_school, self.aura_type))
        elif self.suffix == "EXTRA_ATTACKS":
            ret = ret + (", amount=%s" % self.amount)
        elif self.suffix in ["AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH"]:
            ret = ret + (", aura type=%s, remaining=%s, unknown1=%s, unknown2=%s" % (self.aura_type, self.remaining, self.unknown1, self.unknown2))
        elif self.suffix == "AURA_BROKEN":
            ret = ret + (", aura type=%s" % self.aura_type)
        elif self.suffix in ["AURA_APPLIED_DOSE", "AURA_REMOVED_DOSE"]:
            ret = ret + (", aura type=%s, amount=%s" % (self.aura_type, self.amount))
        elif self.suffix == "CAST_FAILED":
            ret = ret + (", failed type=%s" % self.failed_type)

        return ret

    def __build_arguments(self):
        if self.type_name in ["ENCHANT_APPLIED", "ENCHANT_REMOVED"]:
            self.__spell_name = self.__arguments.pop(0)
            self.__item_id = self.__arguments.pop(0)
            self.__item_name = self.__arguments.pop(0)

        if not self.prefix and not self.suffix:
            return

        if self.prefix in ["RANGE", "SPELL", "SPELL_PERIODIC", "SPELL_BUILDING"]:
            self.__spell_id = self.__arguments.pop(0)
            self.__spell_name = self.__arguments.pop(0)
            self.__spell_school = Event.spell_school_conv(self.__arguments.pop(0))
        elif self.prefix == "ENVIRONMENTAL":
            self.__environmental_type = self.__arguments.pop(0)

        if self.suffix == "DAMAGE":
            self.__amount = self.__arguments.pop(0)
            self.__overkill = self.__arguments.pop(0)
            self.__school = Event.spell_school_conv(self.__arguments.pop(0))
            self.__resisted = self.__arguments.pop(0)
            self.__blocked = self.__arguments.pop(0)
            self.__absorbed = self.__arguments.pop(0)
            self.__critical = Event.boolean(self.__arguments.pop(0))
            self.__glancing = Event.boolean(self.__arguments.pop(0))
            self.__crushing = Event.boolean(self.__arguments.pop(0))
        elif self.suffix == "MISSED":
            self.__miss_type = self.__arguments.pop(0)
            self.__amount = self.__arguments.pop(0) if len(self.__arguments) > 0 else "0"
        elif self.suffix == "HEAL":
            self.__amount = self.__arguments.pop(0)
            self.__overhealing = self.__arguments.pop(0)
            self.__absorbed = self.__arguments.pop(0)
            self.__critical = Event.boolean(self.__arguments.pop(0))
        elif self.suffix == "ENERGIZE":
            self.__amount = self.__arguments.pop(0)
            self.__power_type = Event.power_type_conv(self.__arguments.pop(0))
        elif self.suffix in ["DRAIN", "LEECH"]:
            self.__amount = self.__arguments.pop(0)
            self.__power_type = Event.power_type_conv(self.__arguments.pop(0))
            self.__extra_amount = self.__arguments.pop(0)
        elif self.suffix in ["INTERRUPT", "DISPEL_FAILED"]:
            self.__extra_spell_id = self.__arguments.pop(0)
            self.__extra_spell_name = self.__arguments.pop(0)
            self.__extra_school = Event.spell_school_conv(self.__arguments.pop(0))
        elif self.suffix in ["DISPEL", "STOLEN", "AURA_BROKEN_SPELL"]:
            self.__extra_spell_id = self.__arguments.pop(0)
            self.__extra_spell_name = self.__arguments.pop(0)
            self.__extra_school = Event.spell_school_conv(self.__arguments.pop(0))
            self.__aura_type = self.__arguments.pop(0)
        elif self.suffix == "EXTRA_ATTACKS":
            self.__amount = self.__arguments.pop(0)
        elif self.suffix in ["AURA_APPLIED", "AURA_REMOVED", "AURA_REFRESH"]:
            self.__aura_type = self.__arguments.pop(0)
            self.__remaining = self.__arguments.pop(0) if len(self.__arguments) > 0 else "0"
            self.__unknown1 = self.__arguments.pop(0) if len(self.__arguments) > 0 else "0"
            self.__unknown2 = self.__arguments.pop(0) if len(self.__arguments) > 0 else "0"
        elif self.suffix == "AURA_BROKEN":
            self.__aura_type = self.__arguments.pop(0)
        elif self.suffix in ["AURA_APPLIED_DOSE", "AURA_REMOVED_DOSE"]:
            self.__aura_type = self.__arguments.pop(0)
            self.__amount = self.__arguments.pop(0)
        elif self.suffix == "CAST_FAILED":
            self.__failed_type = self.__arguments.pop(0)

    # TODO: use this!
    def __pop_argument(self):
        return self.__arguments.pop(0) if len(self.__arguments) > 0 else "0"
