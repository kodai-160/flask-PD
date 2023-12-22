@app.route('/morning/stamp1')
def stamp1():
    comments = Comment.query.all()
    return render_template('/morning/stamp1.html', comments=comments)

@app.route('/morning/stamp2')
def stamp2():
    comments = Comment.query.all()
    return render_template('/morning/stamp2.html', comments=comments)

@app.route('/morning/stamp3')
def stamp3():
    comments = Comment.query.all()
    return render_template('/morning/stamp3.html', comments=comments)

@app.route('/morning/stamp4')
def stamp4():
    comments = Comment.query.all()
    return render_template('/morning/stamp4.html', comments=comments)

@app.route('/morning/stamp5')
def stamp5():
    comments = Comment.query.all()
    return render_template('/morning/stamp5.html', comments=comments)

@app.route('/morning/stamp6')
def stamp6():
    comments = Comment.query.all()
    return render_template('/morning/stamp6.html', comments=comments)

@app.route('/morning/stamp7')
def stamp7():
    comments = Comment.query.all()
    return render_template('/morning/stamp7.html', comments=comments)

@app.route('/morning/stamp8')
def stamp8():
    comments = Comment.query.all()
    return render_template('/morning/stamp8.html', comments=comments)

@app.route('/morning/stamp9')
def stamp9():
    comments = Comment.query.all()
    return render_template('/morning/stamp9.html', comments=comments)