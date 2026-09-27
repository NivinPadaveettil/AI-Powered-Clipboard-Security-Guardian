from pathlib import Path
from flask import Flask, render_template, jsonify, request
import sys

from src.database.sqlite_logger import logger
from src.config.settings_manager import settings_manager
from src.predict import predict
from src.core.risk_scoring import calculate_risk, RISK_TABLE
from src.services.startup_service import StartupService
from src.utils.app_logger import app_logger

BASE_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(WEB_DIR / "templates"),
    static_folder=str(WEB_DIR / "static"),
)


# ============================================================
# Web Routes
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# API Endpoints
# ============================================================

@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        total = logger.get_total_count()
        critical = logger.get_critical_count()
        high = logger.get_high_count()
        medium = logger.get_medium_count()
        safe = logger.get_safe_count()
        avg_confidence = logger.get_average_confidence()
        avg_risk = logger.get_average_risk_score()
        categories = logger.get_category_counts()

        return jsonify({
            "success": True,
            "total": total,
            "critical": critical,
            "high": high,
            "medium": medium,
            "safe": safe,
            "avg_confidence": round(avg_confidence * 100, 2),
            "avg_risk_score": round(avg_risk, 1),
            "categories": [{"category": cat, "count": count} for cat, count in categories],
        })
    except Exception as e:
        app_logger.error(f"Flask API Stats Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        records = logger.fetch_all()
        # Records schema: id, timestamp, category, confidence, risk_score, risk_level, action
        history = []
        for r in records:
            history.append({
                "id": r[0],
                "timestamp": r[1],
                "category": r[2],
                "confidence": round(float(r[3]) * 100, 2),
                "risk_score": r[4],
                "risk_level": r[5],
                "action": r[6],
                "explanation": RISK_TABLE.get(r[2]).explanation if r[2] in RISK_TABLE else "Security analysis record"
            })
        return jsonify({"success": True, "history": history, "count": len(history)})
    except Exception as e:
        app_logger.error(f"Flask API History Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/settings", methods=["GET", "POST"])
def manage_settings():
    if request.method == "GET":
        try:
            settings = settings_manager.get_all()
            db_info = {
                "path": logger.get_database_path(),
                "size_bytes": logger.get_database_size(),
                "total_records": logger.get_total_count(),
                "log_file": app_logger.get_log_file_path()
            }
            return jsonify({"success": True, "settings": settings, "database": db_info})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    elif request.method == "POST":
        try:
            data = request.json or {}
            new_settings = {
                "monitoring_enabled": bool(data.get("monitoring_enabled", True)),
                "auto_clear_enabled": bool(data.get("auto_clear_enabled", True)),
                "clear_timeout": int(data.get("clear_timeout", 15)),
                "notifications_enabled": bool(data.get("notifications_enabled", True)),
                "start_monitoring_automatically": bool(data.get("start_monitoring_automatically", True)),
            }
            settings_manager.save(new_settings)
            StartupService.set_autostart(new_settings["start_monitoring_automatically"])
            app_logger.log_event("WEB_SETTINGS_SAVED", str(new_settings))
            return jsonify({"success": True, "settings": new_settings})
        except Exception as e:
            app_logger.error(f"Flask API Settings Update Error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/predict", methods=["POST"])
def live_predict():
    try:
        data = request.json or {}
        text = data.get("text", "")
        if not text or not text.strip():
            return jsonify({"success": False, "error": "Empty text provided"}), 400

        label, confidence = predict(text)
        risk = calculate_risk(label, confidence)

        return jsonify({
            "success": True,
            "category": risk.category,
            "confidence": round(risk.confidence * 100, 2),
            "risk_score": risk.risk_score,
            "risk_level": risk.risk_level,
            "explanation": risk.explanation,
            "action": risk.action,
            "timeout": risk.timeout,
        })
    except Exception as e:
        app_logger.error(f"Flask Live Predict Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/clear-history", methods=["POST"])
def clear_history():
    try:
        logger.clear_history()
        app_logger.log_event("WEB_CLEAR_HISTORY", "Detection history cleared via web API")
        return jsonify({"success": True, "message": "History cleared successfully"})
    except Exception as e:
        app_logger.error(f"Flask Clear History Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("Starting AI Security Clipboard Guardian Web Server...")
    print("Web Dashboard available at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
