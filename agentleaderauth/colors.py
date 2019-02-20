class Bcolors:
    """
    To use this code, you can do something like
    print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[34m'
    OKBLUEH = OKBLUE + '['
    OKGREEN = '\033[32m'
    OKGREENH = OKGREEN + '['
    WARNING = '\033[33m'
    WARNINGH = WARNING + '['
    FAIL = '\033[31m'
    FAILH = FAIL + '['
    ENDC = '\033[0m'
    ENDCH = ']: ' + ENDC
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ERROR = FAILH + 'ERROR' + ENDCH
