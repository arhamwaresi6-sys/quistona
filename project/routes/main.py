from flask import Blueprint,redirect,render_template,request,url_for,abort,flash
from project.extensions import supabase,db
from flask_login import current_user,login_required
from werkzeug.security import  check_password_hash
import uuid
from project.modules import User,Image,Course,Batch,Semester
from flask import send_file
from io import BytesIO
import requests
from sqlalchemy import case

main = Blueprint("main",__name__)

#index------------------------------------------
@main.route("/")
def index():
    images = db.session.execute(
        db.select(Image).limit(3).order_by(Image.created_at)
    ).scalars().all()
    context = {
        "current_user":current_user,
        "images":images
    }
    return render_template("index.html",**context)



#batches-----------------------------------------
####-----Read>
@main.route("/batches")
def batches():
    batches = db.session.execute(
    db.select(Batch).order_by(
        db.cast(db.func.regexp_replace(Batch.name, '[^0-9]', ''), db.Integer)
    )
).scalars().all()
    context = {
        "current_user":current_user,
        "batches":batches
    }
    return render_template("batches.html",**context)
####-----write>
@main.route("/create_batch",methods=["post"])
def create_batch():
    name = request.form.get("name")
    batch = Batch(
        name = name
    )
    db.session.add(batch)
    db.session.commit()
    return redirect(url_for("main.batches"))
####-----update>
@main.route("/edit_batch/<int:batch_id>", methods=["POST"])
@login_required
def edit_batch(batch_id):
    if current_user.role not in ["admin", "root"]:
        
        return redirect(url_for("main.batches"))

    batch = db.session.get(Batch, batch_id)

    if not batch:
        return redirect(url_for("main.batches"))

    batch.name = request.form.get("name", "").strip()

    if not batch.name:
        return redirect(url_for("main.batches"))

    db.session.commit()

    return redirect(url_for("main.batches"))
####-----delete>
@main.route("/delete_batch/<int:batch_id>")
def delete_batch(batch_id):
    if current_user.role == "admin" or current_user.role == "root":
        batch = db.session.get(Batch, batch_id)

    if batch:
        db.session.delete(batch)
        db.session.commit()
    return redirect(url_for("main.batches"))




#semesters-----------------------------------------
####-----Read>
@main.route("/semesters/<int:batch_id>")
def semesters(batch_id):
    batch = db.session.get(Batch,batch_id)
    semesters = db.session.execute(
            db.select(Semester).where(Semester.batch_id == batch_id).order_by(
                db.cast(db.func.regexp_replace(Semester.name, '[^0-9]', ''), db.Integer)
            )
        ).scalars().all()
    
    context = {
                "current_user":current_user,
                "semesters":semesters,
                "batch":batch
            }
    return render_template("semesters.html",**context)
####-----write>
@main.route("/create_semester/<int:batch_id>",methods=["post"])
def create_semester(batch_id):
    if current_user.role not in ["admin", "root"]:
            return redirect(url_for("main.semesters"))
    name = request.form.get("name")
    semester = Semester(
        name = name,
        batch_id = batch_id
    )
    db.session.add(semester)
    db.session.commit()
    return redirect(url_for("main.semesters",batch_id = batch_id))
####-----update>
@main.route("/edit_semester/<int:semester_id>", methods=["POST"])
@login_required
def edit_semester(semester_id):
    if current_user.role not in ["admin", "root"]:
        
        return redirect(url_for("main.index"))

    semester = db.session.get(Semester, semester_id)

    if not semester:
        return redirect(url_for("main.batches"))
    batch_id = semester.batch_id
    semester.name = request.form.get("name", "").strip()

    if not semester.name:
        return redirect(url_for("main.semesters",batch_id=batch_id))

    db.session.commit()

    return redirect(url_for("main.semesters",batch_id = batch_id))
####-----delete>
@main.route("/delete_semester/<int:semester_id>")
def delete_semester(semester_id):
    if current_user.role == "admin" or current_user.role == "root":
        semester = db.session.get(Semester, semester_id)
    batch_id = None
    if semester:
        batch_id = semester.batch_id
        db.session.delete(semester)
        db.session.commit()
    if not batch_id:
        return redirect(url_for("main.batches"))
    return redirect(url_for("main.semesters",batch_id= batch_id))




#courses-----------------------------------------
####-----read>
@main.route("/courses/<int:semester_id>")
def courses(semester_id):
    semester=db.session.get(Semester,semester_id)
    return render_template("courses.html",current_user= current_user,semester=semester)
####-----write>
@main.route("/create_course/<int:semester_id>",methods=["post"])
def create_course(semester_id):
    if current_user.role == 'root' or current_user.role == 'admin':
        name = request.form.get("name")
        course = Course(
            name=name,
            semester_id = semester_id
        )
        db.session.add(course)
        db.session.commit()
    return redirect(url_for("main.courses",semester_id=semester_id))
####-----update>
@main.route("/edit_course/<int:course_id>", methods=["POST"])
@login_required
def edit_course(course_id):
    if current_user.role not in ["admin", "root"]:
        
        return redirect(url_for("main.index"))

    course = db.session.get(Course, course_id)

    if not course:
        return redirect(url_for("main.batches"))
    semester_id = course.semester_id
    course.name = request.form.get("name", "").strip()

    if not course.name:
        return redirect(url_for("main.courses",semester_id=semester_id))

    db.session.commit()

    return redirect(url_for("main.courses",semester_id=semester_id))
####-----delete>
@main.route("/create_course/<int:course_id>")
def delete_course(course_id):
    course = db.session.get(Course,course_id)
    semester_id = course.semester_id
    if current_user.role == 'root' or current_user.role == 'admin':
        if course:
            db.session.delete(course)
            db.session.commit()
    return redirect(url_for("main.courses",semester_id=semester_id))





#questions-----------------------------------------
@main.route("/questions/<int:course_id>")
def questions(course_id):
    course = db.session.get(Course,course_id)
    if course == None:
        return redirect(url_for("main.courses")) 
    context = {
            "current_user":current_user,
            "course":course
        }
    return render_template("questions.html",**context)




@main.route("/supplementary/<int:course_id>")
def supplementary(course_id):
    course = db.session.get(Course,course_id)
    if course == None:
        return redirect(url_for("main.courses")) 
    context = {
                "current_user":current_user,
                "course":course
            }
    return render_template("supplementary.html",**context)
















@main.route("/upload/<int:course_id>/<course_type>",methods=["POST"])
@login_required
def upload(course_id,course_type):
    type = request.form.get("type")
    file = request.files.get("image")
    if file and file.filename:
        ext = file.filename.rsplit(".",1)[-1]
        filename = f'{uuid.uuid4()}.{ext}'
        file_path = f"questions/{filename}"
        supabase.storage.from_("Questona").upload(
            path=file_path,
            file=file.read(),
            file_options={
                "content-type": file.content_type
            }
        )
        url = supabase.storage.from_("Questona").get_public_url(file_path)
        image = Image(
            url=url,
            user_id=current_user.id,
            course_id=course_id,
            type=type,
            course_type = course_type
        )

        db.session.add(image)
        db.session.commit()
    return redirect(url_for('main.questions',course_id = course_id))

@main.route("/delete_image/<int:image_id>")
@login_required
def delete_image(image_id):
    image = db.session.get(Image, image_id)

    if not image:
        abort(404)

    if image.user_id != current_user.id and current_user.role not in ["admin", "root"]:
        abort(403)

    file_path = image.url.split("/storage/v1/object/public/Questona/", 1)

    if len(file_path) != 2:
        abort(400, description="Invalid Supabase image URL")

    supabase.storage.from_("Questona").remove([file_path[1]])

    db.session.delete(image)
    db.session.commit()

    return redirect(url_for("main.questions", course_id=image.course_id))
@main.route("/edit_image/<int:image_id>", methods=["POST"])
@login_required
def edit_image(image_id):
    image = db.session.get(Image, image_id)

    if not image:
        abort(404)

    if image.user_id != current_user.id and current_user.role not in ["admin", "root"]:
        abort(403)

    image.type = request.form.get("name", "").strip()

    if not image.type:
        abort(400)

    db.session.commit()

    return redirect(url_for("main.questions", course_id=image.course_id))


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@main.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")

    if not name or not email:
        return redirect(url_for("main.profile"))

    existing_user = db.session.execute(
        db.select(User).where(
            User.email == email,
            User.id != current_user.id
        )
    ).scalar_one_or_none()

    if existing_user:
        return redirect(url_for("main.profile"))

    if new_password:
        if not current_password:
            return redirect(url_for("main.profile"))

        if not check_password_hash(
            current_user.password_hash, current_password
        ):
            return redirect(url_for("main.profile"))

        if len(new_password) < 8:
            return redirect(url_for("main.profile"))

        current_user.password = new_password

    current_user.name = name
    current_user.email = email

    db.session.commit()

    return redirect(url_for("main.profile"))
from flask import send_file
from io import BytesIO
import requests

@main.route("/download_image/<int:image_id>")
@login_required
def download_image(image_id):
    image = db.session.get(Image, image_id)

    if not image:
        abort(404)

    response = requests.get(image.url, timeout=20)

    if response.status_code != 200:
        abort(502)

    return send_file(
        BytesIO(response.content),
        mimetype=response.headers.get("Content-Type", "application/octet-stream"),
        as_attachment=True,
        download_name=f"question_{image.id}.jpg"
    )
@main.route("/users")
def users():
    users = db.session.execute(
        db.select(User).order_by(
            case(
                (User.role == "root", 1),
                (User.role == "admin", 2),
                (User.role == "user", 3),
                else_=4
            ),
            User.name.asc()
        )
    ).scalars().all()

    return render_template(
        "users.html",
        users=users,
        current_user=current_user
    )
@main.route("/users/<int:user_id>/change-role", methods=["POST"])
@login_required
def change_user_role(user_id):
    # Only root can manage users
    if current_user.role != "root":
        abort(403)

    user = db.session.get(User, user_id)

    if not user:
        abort(404)

    # Prevent changing your own role
    if user.id == current_user.id:
        flash("You cannot change your own role.", "error")
        return redirect(url_for("main.users"))

    new_role = request.form.get("role")

    if new_role not in ["user", "admin"]:
        abort(400)

    user.role = new_role
    db.session.commit()

    flash(f"{user.name}'s role has been changed to {new_role}.", "success")
    return redirect(url_for("main.users"))


@main.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    # Only root can delete users
    if current_user.role != "root":
        abort(403)

    user = db.session.get(User, user_id)

    if not user:
        abort(404)

    # Prevent deleting yourself or another root
    if user.id == current_user.id or user.role == "root":
        flash("You cannot delete this account.", "error")
        return redirect(url_for("main.users"))

    db.session.delete(user)
    db.session.commit()

    flash(f"{user.name}'s account has been deleted.", "success")
    return redirect(url_for("main.users"))