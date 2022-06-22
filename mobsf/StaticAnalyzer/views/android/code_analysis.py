# -*- coding: utf_8 -*-
"""Module holding the functions for code analysis."""

import logging
from pathlib import Path

from django.conf import settings

from mobsf.MobSF.utils import filename_from_path
from mobsf.StaticAnalyzer.views.common.shared_func import (
    url_n_email_extract,
)
from mobsf.StaticAnalyzer.views.sast_engine import (
    niap_scan,
    scan,
)
import linecache
import re

logger = logging.getLogger(__name__)


def code_analysis(app_dir, typ, manifest_file, md5):
    """Perform the code analysis."""
    try:
        root = Path(settings.BASE_DIR) / 'StaticAnalyzer' / 'views'
        code_rules = root / 'android' / 'rules' / 'android_rules.yaml'
        api_rules = root / 'android' / 'rules' / 'android_apis.yaml'
        niap_rules = root / 'android' / 'rules' / 'android_niap.yaml'
        code_findings = {}
        api_findings = {}
        email_n_file = []
        url_n_file = []
        url_list = []
        app_dir = Path(app_dir)
        if typ == 'apk':
            src = app_dir / 'java_source'
        elif typ == 'studio':
            src = app_dir / 'app' / 'src' / 'main' / 'java'
            kt = app_dir / 'app' / 'src' / 'main' / 'kotlin'
            if not src.exists() and kt.exists():
                src = kt
        elif typ == 'eclipse':
            src = app_dir / 'src'
        src = src.as_posix() + '/'
        skp = settings.SKIP_CLASS_PATH
        logger.info('Code Analysis Started on - %s',
                    filename_from_path(src))
        logger.info(src)
        # Code and API Analysis
        code_findings = scan(
            code_rules.as_posix(),
            {'.java', '.kt'},
            [src],
            skp)
        api_findings = scan(
            api_rules.as_posix(),
            {'.java', '.kt'},
            [src],
            skp)
        # NIAP Scan
        broacast_list=[]
        if 'api_send_broadcast' in api_findings:
            for k in api_findings['api_send_broadcast']['files'].keys():
                path=str(Path(settings.UPLD_DIR)/ md5  /'java_source'/ k )
                path=path.replace('\\','/')
                end_line_no_list=api_findings['api_send_broadcast']['files'][k].split(',')
                end_line_no_int_list = [int(i) for i in end_line_no_list]
              
                for end_line_no in end_line_no_int_list:
                    broadcast={
                        'action':'Empty',
                        'target_package':'Empty',
                        'file_name':k,
                        'line_number':end_line_no
                    }
                    start_line_no=0
                    try:
                        with open(path, 'r') as fp:
                            x = fp.readlines()
                            for i in range(end_line_no,0,-1):
                                line=x[i-1]
                                package_re=re.match(r".*(\.setPackage\((.*)\);).*",line)
                                intent_re=re.match(r"( )*Intent (.*)=( )?new Intent(.*);( )*", line)
                                action_re=re.match(r".*(\.setAction\((.*)\);).*",line)
                                if(package_re):
                                    broadcast['target_package']=re.sub('[^A-Za-z0-9.]+', '', package_re.group(2))

                                elif(action_re):
                                    broadcast['action']=re.sub('[^A-Za-z0-9.]+', '', action_re.group(2))                               

                                elif intent_re:
                                    if broadcast['action']=='Empty':
                                        broadcast['action']=re.sub('[^A-Za-z0-9.]+', '', intent_re.group(4))
                                    start_line_no=i
                                    break
                        broacast_list.append(broadcast)
                    except Exception as e:
                        logger.error("Error reading the file name : "+path)

    
          
    
        logger.info('Running NIAP Analyzer')
        niap_findings = niap_scan(
            niap_rules.as_posix(),
            {'.java', '.xml'},
            [src],
            manifest_file,
            None)
        # Extract URLs and Emails
        for pfile in Path(src).rglob('*'):
            if (
                (pfile.suffix in ('.java', '.kt')
                    and any(skip_path in pfile.as_posix()
                            for skip_path in skp) is False)
            ):
                content = None
                try:
                    content = pfile.read_text('utf-8', 'ignore')
                    # Certain file path cannot be read in windows
                except Exception:
                    continue
                relative_java_path = pfile.as_posix().replace(src, '')
                urls, urls_nf, emails_nf = url_n_email_extract(
                    content, relative_java_path)
                url_list.extend(urls)
                url_n_file.extend(urls_nf)
                email_n_file.extend(emails_nf)
        logger.info('Finished Code Analysis, Email and URL Extraction')
        code_an_dic = {
            'api': api_findings,
            'findings': code_findings,
            'niap': niap_findings,
            'urls_list': url_list,
            'urls': url_n_file,
            'emails': email_n_file,
            'broadcasts':broacast_list
        }
        logger.info(code_findings)
    
       
        return code_an_dic
    except Exception as e :
        logger.exception('Performing Code Analysis')
        logger.info(str(e))
