import math
import string

# =========================
# PASSWORD STRENGTH
# =========================

def calculate_entropy(password):
    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)
    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

# =========================
# PASSWORD SCORE
# =========================

def password_score(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    return score

# =========================
# PASSWORD LABEL
# =========================

def password_label(score):
    labels = {
        0: "CRITICAL",
        1: "VERY WEAK",
        2: "WEAK",
        3: "MEDIUM",
        4: "GOOD",
        5: "STRONG",
        6: "VERY STRONG"
    }
    return labels.get(score)

# =========================
# ESTIMATED CRACK TIME
# =========================

def estimate_crack_time(entropy):
    seconds = 2 ** entropy / 1_000_000_000
    minute = 60
    hour = 3600
    day = 86400
    year = 31536000

    if seconds < minute:
        return f"{int(seconds)} seconds"
    elif seconds < hour:
        return f"{int(seconds / minute)} minutes"
    elif seconds < day:
        return f"{int(seconds / hour)} hours"
    elif seconds < year:
        return f"{int(seconds / day)} days"
    else:
        return f"{int(seconds / year)} years"

# =========================
# FULL SECURITY ANALYSIS
# =========================

def analyze_password(password):
    entropy = calculate_entropy(password)
    score = password_score(password)
    label = password_label(score)
    crack_time = estimate_crack_time(entropy)

    return {
        "entropy": entropy,
        "score": score,
        "label": label,
        "crack_time": crack_time
    }