import re
from ConfigParser import ConfigParser


class ConfigLoader(object):

    sect_actions = {'Encoding': lambda x: x,
                    'Data': lambda x: x,
                    'Span': lambda x: int(x),
                    'Extension': lambda x: x,
                    'Regex': lambda x: re.compile(x),
                    'Match': lambda x: x.replace(' ', '')}

    def __init__(self, filename):
        self.settings = self.loadConfig(filename)

    @classmethod
    def readParam(cls, config, option, section, settings):
        opt, sect, sett = option, section, settings
        try:
            sett[opt] = config.get(sect, opt)
            if sett[opt] == -1:
                print("skip: %s" % opt)
        except:
            print("exception on %s!" % opt)
            sett[opt] = None

    @classmethod
    def loadConfig(cls, config_file="config.ini"):
        sett = dict()
        config = ConfigParser()
        # ConfigParser parses INI files which are expected to be parsed case-insensitively
        # disable this behaviour by replacing the RawConfigParser.optionxform() function
        config.optionxform = str
        config.read(config_file)
        sections = config.sections()

        for sect in sections:
            options = config.options(sect)
            action = cls.sect_actions[sect]
            for option in options:
                ConfigLoader.readParam(config, option, sect, sett)
                sett[option] = action(sett[option])

        return sett

    def updateConfig(self, config_file):
        sett = dict()
        config = ConfigParser()
        config.optionxform = str
        config.read(config_file)
        sections = config.sections()

        for sect in sections:
            options = config.options(sect)
            action = self.sect_actions[sect]
            for option in options:
                ConfigLoader.readParam(config, option, sect, sett)
                sett[option] = action(sett[option])

        settings = self.settings
        for k, v in sett.iteritems():
            settings[k] = v

        return settings
