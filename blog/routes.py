from flask import render_template, request
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/homepage")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/", defaults={'entry_id': None}, methods=["GET", "POST"])
@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    errors = None
    if entry_id is None:
        entry = Entry()
        form = EntryForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                entry.title = form.title.data
                entry.body = form.body.data
                entry.is_published = form.is_published.data
                db.session.add(entry)
                db.session.commit()
            else:
                errors = form.errors
    else:   
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
            else:
                errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)
