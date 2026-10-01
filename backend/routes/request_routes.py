from flask import Blueprint, render_template, jsonify, request, current_app, g
from backend.auth.decorators import participant_required
from backend.models.event import Event
from backend.models.request import Request
from backend.models.review import Review

request_bp=Blueprint('requests',__name__)


@request_bp.get('/dashboard')
@participant_required
def dashboard():
    return render_template('dashboard.html',requests=Request.for_user(current_app.db,g.user['id']))


@request_bp.get('/create_request')
@participant_required
def create_page():
    return render_template('create_request.html')


@request_bp.route('/api/requests',methods=['GET','POST'])
@participant_required
def requests_api():
    if request.method=='GET':
        return jsonify(success=True,requests=Request.for_user(current_app.db,g.user['id']))
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(success=False,message='Ожидается объект JSON'),400
    payment=data.get('payment_method')
    if payment not in ('При очном посещении','СБП'):
        return jsonify(success=False,message='Выберите способ оплаты'),400
    event=Event(data.get('name'),data.get('date'),data.get('start_time'),data.get('place'),current_app.db)
    ok,result=event.save()
    if not ok:
        return jsonify(success=False,message=result),400
    booking=Request(g.user['id'],result,payment,current_app.db)
    ok,result=booking.save()
    return jsonify(success=ok,**({'request_id':result,'redirect':'/dashboard'} if ok else {'message':result})),201 if ok else 400


@request_bp.post('/api/requests/<int:request_id>/review')
@participant_required
def add_review(request_id):
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(success=False,message='Ожидается объект JSON'),400
    review=Review(request_id,g.user['id'],data.get('text'),data.get('rating'),current_app.db)
    ok,result=review.save()
    return jsonify(success=ok,**({'review_id':result} if ok else {'message':result})),201 if ok else 400
