from flask import Blueprint, render_template, jsonify, request, current_app
from backend.auth.decorators import admin_required
from backend.models.request import Request

admin_bp=Blueprint('admin',__name__)


@admin_bp.get('/admin')
@admin_required
def admin():
    return render_template('admin.html',requests=Request.all(current_app.db))


@admin_bp.get('/api/admin/requests')
@admin_required
def all_requests():
    return jsonify(success=True,requests=Request.all(current_app.db))


@admin_bp.put('/api/admin/requests/<int:request_id>')
@admin_required
def change_status(request_id):
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(success=False,message='Ожидается объект JSON'),400
    ok,msg=Request.update_status(current_app.db,request_id,data.get('status_id'))
    return jsonify(success=ok,message=msg),200 if ok else 400
