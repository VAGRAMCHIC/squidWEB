import os, re, subprocess
import bcrypt
from datetime import datetime


from flask import Blueprint, render_template, request, redirect, url_for
from flask import session


from flask_login import login_required, current_user
from flask_login.mixins import AnonymousUserMixin

from app.models import Users
from app.database import db

man_bp = Blueprint('manager', __name__, url_prefix='/manage')

LOG_PATTERN = re.compile(
    r'^(\d+\.\d+)\s+'        # Timestamp
    r'(\d+)\s+'               # Duration (ms)
    r'(\S+)\s+'               # Client IP
    r'(\S+)/(\d+)\s+'         # Cache status/HTTP status
    r'(\d+)\s+'               # Bytes
    r'(\S+)\s+'               # Method
    r'(\S+)\s+'               # URL
    r'(\S+)\s+'               # Hierarchy code
    r'(\S+).*'                # Content type
)


def grep_search(filename, pattern, index):
    result = subprocess.run(
        ['grep', pattern, filename],
        stdout=subprocess.PIPE,
        text=True
    ).stdout.striplines()
    res = result[:]
    return result.stdout.splitlines()

def parse_squid_log(line):
    """Парсинг строки лога в структуру данных"""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    
    return {
        'timestamp': float(match.group(1)),
        'datetime': datetime.fromtimestamp(float(match.group(1))).strftime('%Y-%m-%d %H:%M:%S'),
        'duration': int(match.group(2)),
        'client_ip': match.group(3),
        'cache_status': match.group(4),
        'http_status': int(match.group(5)),
        'bytes': int(match.group(6)),
        'method': match.group(7),
        'url': match.group(8),
        'hierarchy': match.group(9),
        'content_type': match.group(10)
    }


@man_bp.route('/logs',methods=['GET'])
@login_required
def get_logs():
    if isinstance(current_user, AnonymousUserMixin):
        username=""
        return redirect("account.login")
    else:
        username=current_user.username
    
    log_path = "test_log/access.log"
    logs = []

    try:
        with open(log_path, 'r') as f:
            # Чтение последних 100 строк (реверс для новых записей сверху)
            for line in list(f.readlines())[-100:]:
                parsed = parse_squid_log(line)
                if parsed:
                    logs.append(parsed)
            logs.reverse()  # Новые записи в начале
    except Exception as e:
        logs = [{'error': f'Ошибка чтения файла: {str(e)}'}]
    
    return render_template('logsView.html', logs=logs, username=username)



@man_bp.route('/logs',methods=['POST'])
@login_required
def search_logs():
    if isinstance(current_user, AnonymousUserMixin):
        username=""
        return redirect("account.login")
    else:
        username=current_user.username
    
    log_path = "test_log/access.log"
    logs = []

    try:
        pattern = request.form["s_pattern"]
        lines = grep_search(log_path, pattern)
    except Exception as e:
        print(e)
        logs = [{'error': f'Ошибка чтения файла: {str(e)}'}]
        return render_template('logsView.html', logs=logs, username=username)
    
        
    return render_template('logsView.html', logs=logs, username=username)



@man_bp.route('/logs/<log_path>',methods=['GET','POST'])
@login_required
def show_found_logs(log_path):
    if isinstance(current_user, AnonymousUserMixin):
        username=""
        return redirect("account.login")
    else:
        username=current_user.username
    
    log_path = log_path
    logs=[]
    return log_path

    

