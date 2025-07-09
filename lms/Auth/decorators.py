from django.core.exceptions import PermissionDenied


# to restrict access only to librarian
def librarian_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_librarian', False):#if theis_librarian is false
            raise PermissionDenied
        #if user is librarian,call view with argument
        return view_func(request, *args, **kwargs)
    return _wrapped_view 

""" Some views are added extra just for the role of librarian and these can be only accesed
if the user is a librarian, here the function viewfunc is wrapped for additional info with args and kwargs cause
we might not know the number and type of parameters

the wrapped hides both the views and adds functionalities
"""