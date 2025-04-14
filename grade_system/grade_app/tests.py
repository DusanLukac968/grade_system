class HrUserUpdate(generic.edit.CreateView):
    form_class = HRUserUpdateForm
    template_name = 'grade_system/hr_user_update.html'

    
    
    
    def post(self, request, pk):
        if not request.user.user_level == 0:
            messages.info/request, "You are not obligated to enter this page!"
            return redirect("main_page")
        form = self.form_class(request.POST)

        if form.is_valid():
            user_level = form.cleaned_data["namuser_levele"]
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            tel = form.cleaned_data["tel"]
            try:
                get_user= request.POST.get('update_data_for_user')
                update_this_user = User.objects.get(pk= get_user)
                old_level = update_this_user.user_level
                update_this_user.POST('user_level')
            except:
                messages.error(request, "User doesn't exist")
                return redirect("main_page")
            
            update_this_user.user_level = user_level
            update_this_user.name = name
            update_this_user.surname = surname
            update_this_user.date_of_birth = date_of_birth
            update_this_user.tel = tel
            update_this_user.save()
            if old_level != update_this_user.user_level:
                if old_level == 2:
                    get_teacher = Teacher.objects.get(user = get_user)
                    try:
                        get_teacher.delete()
                        messages.success(request, f"Teacher profile for user {update_this_user.name} {update_this_user.surname} deleted continue to new register")
                        if int(update_this_user.user_level) == 3:
                            return redirect("student_advance_register")
                        elif int(update_this_user.user_level) == 4:
                            return redirect("parent_advance_register")
                    except Teacher.DoesNotExist:
                        messages.error(request, "1Somthing went wrong :(")
                elif old_level == 3:
                    get_student = Student.objects.get(user = get_user)
                    try:
                        get_student.delete()
                        messages.success(request, f"Student profile for user {update_this_user.name} {update_this_user.surname}  deleted continue to new register")
                        if int(update_this_user.user_level) == 2:
                            return redirect("teacher_advance_register")
                        elif int(update_this_user.user_level) == 4:
                            return redirect("parent_advance_register")
                    except Student.DoesNotExist:
                        messages.error(request, f"Somthing went wrong :(")
                elif old_level == 4:
                    get_parent = Student.objects.get(user = get_user)
                    try:
                        get_parent.delete()
                        messages.success(request, f"Parents profile for user {update_this_user.name} {update_this_user.surname} deleted continue to new register")
                        if int(update_this_user.user_level)==3:
                            return redirect("student_advance_register")
                        elif int(update_this_user.user_level)==2:
                            return redirect("teacher_advance_register")
                    except Parent.DoesNotExist:
                        messages.error(request, "3Somthing went wrong :(")
        return render(request, self.template_name, {"form": form})