import os
import sys
import time
import datetime

from glob import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

_quit = False
_save = ""

HEADER = """
################################
##                            ##
##  Full Auto Cookie Clicker  ##
##  v2.6                      ##
##                            ##
################################
"""

COOKIE = """
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;11;3;1m \033[38;2;45;23;10m_\033[38;2;56;31;16m_\033[38;2;79;46;22ma\033[38;2;89;52;27mm\033[38;2;82;46;24mm\033[38;2;72;40;24mm\033[38;2;82;48;28mm\033[38;2;79;47;24mg\033[38;2;55;30;15m,\033[38;2;52;29;13m_\033[38;2;20;8;3m_\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;3;1;1m \033[38;2;57;33;19m_\033[38;2;84;50;29mg\033[38;2;107;66;39mm\033[38;2;113;69;40mC\033[38;2;117;72;41mC\033[38;2;127;86;54mC\033[38;2;126;82;50mC\033[38;2;122;79;43mC\033[38;2;136;90;51mC\033[38;2;129;83;47mC\033[38;2;119;75;42mC\033[38;2;126;80;44mC\033[38;2;127;82;46mC\033[38;2;125;79;43mC\033[38;2;117;71;38mC\033[38;2;93;55;28mm\033[38;2;81;47;24mm\033[38;2;61;34;17mg\033[38;2;8;2;1m_\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;75;44;23mu\033[38;2;103;60;32mi\033[38;2;109;66;37mX\033[38;2;126;86;54mC\033[38;2;135;90;53mC\033[38;2;126;80;42mC\033[38;2;114;72;44mX\033[38;2;100;64;48mX\033[38;2;115;78;56mX\033[38;2;119;81;56mC\033[38;2;131;89;54mC\033[38;2;129;87;51mi\033[38;2;127;87;52mi\033[38;2;129;86;50mC\033[38;2;146;106;66mi\033[38;2;149;108;65mi\033[38;2;134;87;46mi\033[38;2;123;80;46mC\033[38;2;126;80;44mC\033[38;2;130;86;49mC\033[38;2;99;59;33mN\033[38;2;72;40;20mg\033[38;2;16;5;3m_\033[39m \033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;65;36;18m_\033[38;2;113;69;37mi\033[38;2;130;84;49mC\033[38;2;125;81;48mi\033[38;2;131;86;49mi\033[38;2;119;74;39mC\033[38;2;136;94;54mi\033[38;2;153;108;61m:\033[38;2;152;109;66mi\033[38;2;120;82;50mC\033[38;2;102;67;43mQ\033[38;2;90;56;45mQ\033[38;2;91;58;46mQ\033[38;2;121;86;56mX\033[38;2;153;108;60mB\033[38;2;152;112;67mi\033[38;2;133;92;55mi\033[38;2;153;113;70m:\033[38;2;150;108;63m:\033[38;2;154;111;67mi\033[38;2;147;102;59mi\033[38;2;143;98;57mi\033[38;2;122;80;46mC\033[38;2;117;73;41mC\033[38;2;101;60;32mN\033[38;2;48;24;10mL\033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[38;2;52;28;14m_\033[38;2;102;58;32mX\033[38;2;128;83;46mC\033[38;2;140;97;59mC\033[38;2;129;90;57mC\033[38;2;127;87;50mC\033[38;2;134;93;55mi\033[38;2;157;114;66m:\033[38;2;158;116;68mi\033[38;2;149;109;66mi\033[38;2;148;108;65m:\033[38;2;144;106;65mi\033[38;2;147;106;64mi\033[38;2;158;117;74m:\033[38;2;160;119;74m:\033[38;2;175;140;95mB\033[38;2;161;120;77mQ\033[38;2;147;105;63mB\033[38;2;143;103;63mi\033[38;2;132;95;61mi\033[38;2;153;112;69mi\033[38;2;150;106;61mi\033[38;2;150;107;62mi\033[38;2;151;111;69mi\033[38;2;140;97;58mi\033[38;2;123;77;42mC\033[38;2;114;71;41mC\033[38;2;47;23;8mk\033[39m \033[39m 
\033[39m \033[39m \033[39m \033[38;2;37;17;6m \033[38;2;106;64;36mC\033[38;2;117;73;42mC\033[38;2;124;82;49mC\033[38;2;126;83;49mC\033[38;2;145;102;58mi\033[38;2;147;103;59mi\033[38;2;156;114;66m:\033[38;2;157;115;69mB\033[38;2;167;128;83mB\033[38;2;123;85;55mi\033[38;2;119;80;52mC\033[38;2;94;57;44mX\033[38;2;105;71;53mX\033[38;2;126;91;62mN\033[38;2;182;154;117m[\033[38;2;191;166;131m'\033[38;2;188;160;123mF\033[38;2;177;142;97mq\033[38;2;158;118;73mB\033[38;2;124;87;60mC\033[38;2;121;85;62mC\033[38;2;106;72;59mC\033[38;2;93;59;53mX\033[38;2;126;85;50mC\033[38;2;137;98;62mi\033[38;2;131;89;53mC\033[38;2;124;80;47mC\033[38;2;104;63;38mC\033[38;2;42;22;15mL\033[39m 
\033[39m \033[39m \033[39m \033[38;2;90;51;27md\033[38;2;109;66;38mX\033[38;2;117;74;43mX\033[38;2;128;83;49mC\033[38;2;138;94;53mi\033[38;2;154;110;64mi\033[38;2;158;119;73mK\033[38;2;171;132;84mD\033[38;2;168;130;85m0\033[38;2;140;110;77mN\033[38;2;81;45;39mQ\033[38;2;100;66;56mX\033[38;2;104;73;63mX\033[38;2;90;53;45mQ\033[38;2;87;52;46mQ\033[38;2;99;69;59mX\033[38;2;175;153;124my\033[38;2;191;165;128m:\033[38;2;182;151;108m2\033[38;2;183;155;121my\033[38;2;129;96;65mN\033[38;2;108;85;76mX\033[38;2;99;73;65mX\033[38;2;87;55;49mX\033[38;2;92;59;44mQ\033[38;2;145;104;62mi\033[38;2;119;79;49mi\033[38;2;131;86;50mC\033[38;2;114;70;39mC\033[38;2;92;54;30mB\033[39m 
\033[39m \033[39m \033[39m \033[38;2;109;67;42mX\033[38;2;117;74;44mC\033[38;2;123;80;48mC\033[38;2;129;89;55mi\033[38;2;137;96;57mi\033[38;2;159;119;72mB\033[38;2;170;137;97mk\033[38;2;170;134;89m8\033[38;2;169;138;99mX\033[38;2;115;85;59mX\033[38;2;76;40;34mQ\033[38;2;84;48;41mQ\033[38;2;81;44;39mQ\033[38;2;81;45;38mQ\033[38;2;83;49;37mQ\033[38;2;127;101;77mN\033[38;2;173;148;113mK\033[38;2;165;133;93m4\033[38;2;168;141;104mK\033[38;2;163;130;88mA\033[38;2;153;123;88mQ\033[38;2;161;133;98mX\033[38;2;171;139;99mG\033[38;2;161;120;71mX\033[38;2;152;111;69mH\033[38;2;152;111;67mi\033[38;2;137;94;53mi\033[38;2;135;92;55mi\033[38;2;122;77;41mC\033[38;2;114;71;40mC\033[38;2;12;3;2m 
\033[39m \033[39m \033[39m \033[38;2;101;60;36mX\033[38;2;113;68;36mX\033[38;2;117;72;41mC\033[38;2;134;89;51mi\033[38;2;152;113;72mi\033[38;2;148;110;67m:\033[38;2;163;128;83mQ\033[38;2;176;146;105mD\033[38;2;188;163;128mZ\033[38;2;185;156;117m(\033[38;2;181;154;119mD\033[38;2;151;122;86mN\033[38;2;136;106;72mN\033[38;2;137;108;76mN\033[38;2;187;162;126m[\033[38;2;188;162;124m,\033[38;2;189;163;125m,\033[38;2;197;177;145m7\033[38;2;178;148;109mo\033[38;2;162;130;88mv\033[38;2;178;150;112mb\033[38;2;184;156;117mK\033[38;2;159;124;85mV\033[38;2;156;120;81mH\033[38;2;153;114;75mQ\033[38;2;137;98;60mi\033[38;2;129;86;50mi\033[38;2;128;83;48mC\033[38;2;115;71;38mC\033[38;2;112;67;36mX\033[38;2;24;11;7m 
\033[39m \033[39m \033[39m \033[38;2;79;43;20m]\033[38;2;110;65;36mX\033[38;2;120;76;43mC\033[38;2;125;80;44mC\033[38;2;146;105;64mi\033[38;2;157;118;74m:\033[38;2;166;131;89mQ\033[38;2;168;135;95mP\033[38;2;169;138;97mH\033[38;2;156;132;105mk\033[38;2;171;142;106m0\033[38;2;176;148;109ma\033[38;2;166;137;101m]\033[38;2;182;153;115mK\033[38;2;185;161;127mA\033[38;2;180;155;119m0\033[38;2;186;159;121m]\033[38;2;192;171;140ms\033[38;2;184;155;115m=\033[38;2;169;141;106mf\033[38;2;155;122;85mG\033[38;2;148;120;94mm\033[38;2;138;108;81mD\033[38;2;90;58;51mX\033[38;2;115;77;47mX\033[38;2;128;85;50mC\033[38;2;121;77;47mC\033[38;2;118;76;44mX\033[38;2;103;60;33mX\033[38;2;76;40;22mN\033[39m 
\033[39m \033[39m \033[39m \033[38;2;53;27;12m]\033[38;2;110;66;37mC\033[38;2;122;80;47mC\033[38;2;142;98;59mi\033[38;2;139;95;52mi\033[38;2;144;102;60mi\033[38;2;143;100;56mi\033[38;2;152;117;78mQ\033[38;2;122;88;56mC\033[38;2;92;58;38mQ\033[38;2;139;114;89mN\033[38;2;156;127;95mb\033[38;2;139;110;83mm\033[38;2;144;110;77mB\033[38;2;168;137;101m8\033[38;2;162;127;85md\033[38;2;148;114;78mm\033[38;2;157;123;87mk\033[38;2;160;127;88mm\033[38;2;163;133;98mG\033[38;2;116;83;54mC\033[38;2;109;81;60mX\033[38;2;105;70;41mX\033[38;2;124;85;49mX\033[38;2;134;94;57mC\033[38;2;146;102;59mi\033[38;2;126;84;50mC\033[38;2;114;71;39mC\033[38;2;106;64;39mX\033[38;2;33;14;7m6\033[39m 
\033[39m \033[39m \033[39m \033[39m \033[38;2;64;36;20m]\033[38;2;113;72;46mC\033[38;2;119;79;50mC\033[38;2;129;86;49mi\033[38;2;135;92;54mi\033[38;2;139;94;53mi\033[38;2;133;94;56mi\033[38;2;111;76;47mC\033[38;2;121;89;62mC\033[38;2;96;62;42mC\033[38;2;84;52;47mX\033[38;2;85;51;46mQ\033[38;2;89;57;45mX\033[38;2;145;111;74mi\033[38;2;132;93;54mi\033[38;2;91;59;54mX\033[38;2;95;62;55mX\033[38;2;108;72;53mC\033[38;2;131;95;62mi\033[38;2;155;115;68mi\033[38;2;146;104;62mi\033[38;2;136;97;60mi\033[38;2;131;87;49mi\033[38;2;134;91;52mi\033[38;2;122;80;45mi\033[38;2;120;76;44mC\033[38;2;105;61;33mX\033[38;2;55;28;14mB\033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;36;16;7m"\033[38;2;83;44;25mX\033[38;2;104;61;37mX\033[38;2;106;64;38mX\033[38;2;118;77;48mC\033[38;2;123;78;45mC\033[38;2;110;69;39mX\033[38;2;96;59;34mQ\033[38;2;106;68;41mQ\033[38;2;128;87;52mX\033[38;2;93;57;33mQ\033[38;2;129;89;52mC\033[38;2;149;107;65mi\033[38;2;124;89;57mX\033[38;2;76;40;33mW\033[38;2;69;34;27mW\033[38;2;76;41;35mQ\033[38;2;102;66;41mX\033[38;2;157;115;70mi\033[38;2;152;111;67mi\033[38;2;144;100;58mi\033[38;2;131;86;47mi\033[38;2;124;79;45mC\033[38;2;110;66;38mX\033[38;2;92;50;27mX\033[38;2;45;24;10mP\033[38;2;0;0;0m^\033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;56;29;13mY\033[38;2;88;49;27mX\033[38;2;99;55;29mX\033[38;2;109;66;37mX\033[38;2;122;81;51mC\033[38;2;126;82;47mC\033[38;2;131;86;50mi\033[38;2;129;85;46mi\033[38;2;115;75;45mC\033[38;2;125;81;46mC\033[38;2;132;88;52mi\033[38;2;135;91;53mi\033[38;2;130;86;49mC\033[38;2;136;91;50mC\033[38;2;125;87;53mX\033[38;2;137;94;53mi\033[38;2;131;89;50mi\033[38;2;128;83;44mi\033[38;2;121;81;46mC\033[38;2;109;66;36mC\033[38;2;92;53;33mX\033[38;2;63;32;16mR\033[38;2;18;5;2mF\033[39m \033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;33;14;5m"\033[38;2;69;37;19mN\033[38;2;87;49;27mX\033[38;2;103;61;36mX\033[38;2;108;67;40mX\033[38;2;108;66;38mX\033[38;2;112;68;38mX\033[38;2;115;70;40mX\033[38;2;116;72;41mC\033[38;2;115;72;42mC\033[38;2;113;68;37mC\033[38;2;118;76;47mC\033[38;2;113;71;41mC\033[38;2;115;71;38mC\033[38;2;105;62;35mC\033[38;2;94;53;29mX\033[38;2;67;35;19mN\033[38;2;37;16;8mP\033[38;2;1;0;0m"\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m 
\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[38;2;0;0;0m"\033[38;2;0;0;0m"\033[38;2;30;12;4m"\033[38;2;49;24;10mP\033[38;2;59;30;15mV\033[38;2;68;37;22mN\033[38;2;73;39;22mN\033[38;2;72;38;21mN\033[38;2;74;42;25mN\033[38;2;55;27;12mP\033[38;2;49;22;11mP\033[38;2;40;19;7mP\033[38;2;28;11;3m"\033[38;2;0;0;0m"\033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m \033[39m 
"""[1:-1]

def count_files_in(dir):
    """
    Count files in directory.

    Parameters
    ----------
    dir : str
        directory to search (not recursive)

    Returns
    -------
    int
        number of files

    """

    if os.path.isdir(dir):
        return len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    else:
        os.makedirs(dir)
        return 0

def get_latest_file(dir):
    """
    Return latest modified file path.

    Parameters
    ----------
    dir : str
        directory to search (not recursive)

    Returns
    -------
    str
        latest modified file path

    """
    target = os.path.join(dir, '*')
    files = [(f, os.path.getmtime(f)) for f in glob(target)]
    latest_modified_file_path = sorted(files, key=lambda files: files[1])[-1]
    return latest_modified_file_path[0]

def cc_import_bkp(driver, dir):
    """
    If exists, import latest save file in directory.
    
    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        chromedriver object
    dir : str
        directory to search (not recursive)
    """
    if count_files_in(dir) != 0:
        save = open(get_latest_file(dir), encoding='utf-8')
        driver.execute_script('Game.ImportSaveCode("' + save.read() + '");')
        save.close()

def cc_write_log(driver):
    """
    Write log to stdout

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        chromedriver object
    """

    global _quit
    global _save

    status = {}
    try:
        status = driver.execute_script('''
        return {
            "bakery_name": Game.bakeryName,
            "cookies": Beautify(Game.cookies),
            "cps": Beautify(Game.cookiesPs),
            "next_name": Game.__script_next_name,
            "next_price": Beautify(Game.__script_next_price),
            "ascend_meter": Beautify(Game.ascendMeterLevel),
            "next_ascend_meter": Beautify(Game.__script_next_ascend_meter),
            "ascend_count": Beautify(Game.__script_ascend_count),
            "save_string": Game.WriteSave(1)
        }
        ''')
    except:
        _quit = True
        return

    bakery_name = str(status["bakery_name"])
    cookies = str(status["cookies"])
    cps = str(status["cps"])
    next_name = str(status["next_name"])
    next_price = str(status["next_price"])
    meter = str(status["ascend_meter"])
    next_ascend_meter = str(status["next_ascend_meter"])
    count = str(status["ascend_count"])
    _save = str(status["save_string"])

    log = '\033[39m\033[15F\033[38C' + bakery_name + '\'s bakery'

    log += '\033[2E\033[38C\033[K' + 'Next\t: ' + next_price + ' (' + next_name + ')'
    log += '\033[1E\033[38C\033[K' + 'Cookies\t: ' + cookies
    log += '\033[1E\033[38C\033[K' + 'CpS\t: ' + cps
    #log += '\n'
    log += '\033[2E\033[38C\033[K' + 'Ascend'
    log += '\033[1E\033[38C\033[K' + '  Meter\t: ' + meter + ' / ' + next_ascend_meter
    log += '\033[1E\033[38C\033[K' + '  Count\t: ' + count
    #log += '\n'
    log += '\033[3E\033[38C\033[K' + 'Press Ctrl+C to exit' + '\033[4E'

    sys.stdout.write(log)
    sys.stdout.flush()

def cc_export_save(dir):
    """
    Export save from script
    
    Parameters
    ----------
    dir : str
        directory to save
    """
    global _save
    save = open(os.path.join(dir, 'cc_bkp_' + str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-').replace('-', '') + '.txt'), 'w', encoding='utf-8')
    if _save != "":
        save.write(_save)
    save.close()

def main():

    global _quit
    global _save

    print(HEADER)

    sys.stdout.write("In Preparation")
    sys.stdout.flush()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome('chromedriver', options=options)
    sys.stdout.write(".")
    sys.stdout.flush()
    driver.get('https://orteil.dashnet.org/cookieclicker')
    sys.stdout.write(".")
    sys.stdout.flush()
    
    time.sleep(3)
    sys.stdout.write(".")
    sys.stdout.flush()
    
    cc_import_bkp(driver, './bkp')

    js = open('full-auto-cookie-clicker.js', 'r', encoding='utf-8').read()
    driver.execute_script(js)

    # Erase header and "In Preparation"
    sys.stdout.write('\033[1K')
    sys.stdout.write('\033[1F\033[K' * 8 + '\033[1E')

    sys.stdout.writelines(COOKIE + '\n')
    sys.stdout.flush()

    s = time.time()
    try:
        while True:
            cc_write_log(driver)

            # autosave every 30 minutes
            if time.time() - s > 30 * 60:
                cc_export_save('./bkp')
                s = time.time()

            if _quit:
                raise KeyboardInterrupt

    except KeyboardInterrupt:
        # press Ctrl+C to exit
        sys.stdout.write('\033[2K')
        pass

    cc_export_save('./bkp')

    sys.stdout.write('\033[1F\033[K' * 17)
    sys.stdout.flush()

    try:
        driver.close()
        driver.quit()
    except:
        pass

if __name__ == "__main__":
    main()
