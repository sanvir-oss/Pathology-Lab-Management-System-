from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Test, Booking, TestReport  # make sure you have these models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings


# Helper function to check if a user is staff
def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def admin_bookings(request):
    """
    View for staff to see ALL bookings and manage them.
    """
    # Fetch all bookings from all users
    all_bookings = Booking.objects.all().order_by('-booked_at')

    context = {'bookings': all_bookings}
    return render(request, 'admin_bookings.html', context)


@user_passes_test(is_staff)
def manage_booking(request, booking_id):
    """
    Handles report upload and status change for a specific booking.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'upload_report':
            # Check if a file was actually uploaded
            if 'report_file' in request.FILES:
                report_file = request.FILES['report_file']

                # Check if a report already exists for this booking (optional, but good practice)
                TestReport.objects.update_or_create(
                    booking=booking,
                    defaults={
                        'report_file': report_file,
                        'uploaded_by': request.user
                    }
                )

                # Change status to REPORT_READY
                booking.status = 'REPORT_READY'
                booking.save()
                messages.success(request,
                                 f"Report uploaded and status updated to REPORT_READY for Booking #{booking_id}.")

                # 3. --- EMAIL SENDING LOGIC STARTS HERE ---

                recipient_email = booking.email

                if recipient_email:
                    try:

                        # Email Details
                        subject = f"Pathology Lab Report Ready: {booking.test.name}"
                        message = (
                            f"Dear {booking.full_name},\n\n"
                            f"Your test report for '{booking.test.name}' test is now ready to view! "
                            f"The status of your booking (ID #{booking.id}) has been updated to 'REPORT_READY'.\n\n"
                            f"Make a payment of ₹{booking.test.price} to download your report.\n\n"
                            f"Please log in to your account and go to 'My Bookings' to check the status and download the report after payment confirmation.\n\n"
                            f"Thank you for choosing LabXpert.\n\n"
                            f"Sincerely,\n"
                            f"LabXpert Team"
                        )

                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,  # Sender's email (set in settings.py)
                            [recipient_email],  # Recipient's email
                            fail_silently=False,  # Raise an exception if mail fails
                        )

                        messages.success(request,
                                         f"Report uploaded, status updated, and email successfully sent to {recipient_email}.")

                    except Exception as e:
                        # Log error if email sending failed, but still allow report upload to succeed
                        print(f"ERROR: Failed to send email to {recipient_email}. Reason: {e}")
                        messages.warning(request,
                                         f"Report uploaded and status updated, but email notification failed. Error: {e}")
                else:
                    messages.warning(request, "Report uploaded, but user has no email address configured.")

                # 4. --- EMAIL SENDING LOGIC ENDS HERE ---

            else:
                messages.error(request, "No file selected for upload.")

        elif action == 'confirm_completion' and booking.status == 'REPORT_READY':
            # Only confirm if a report has been uploaded
            booking.status = 'COMPLETED'
            booking.save()
            messages.success(request, f"Booking #{booking_id} confirmed and status set to COMPLETED.")

        # If any action is performed, redirect back to the admin list
        return redirect('admin_bookings')

    # For GET requests (e.g., viewing a detailed management page)
    context = {'booking': booking}
    return render(request, 'manage_booking.html', context)  # You will need to create this template









def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        # 1. Instantiate the form with POST data
        form = UserCreationForm(request.POST)

        # 2. Check if the form data is valid
        if form.is_valid():
            # 3. Save the user
            user = form.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        else:
            # If form is invalid, it will contain error messages
            pass  # The errors will be displayed in the template when rendering the form

    else:
        # For GET requests, create a blank form
        form = UserCreationForm()

        # Pass the form object to the template
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the authenticated user from the form
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            # If invalid, the form will hold the errors
            messages.error(request, "Invalid username or password.")
            # Fall through to render the form with errors

    else:
        # GET request
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})





def home(request):
    """
    Home page - show list of available tests.
    """
    tests = Test.objects.all()
    return render(request, 'home.html', {'tests': tests})


@login_required
def my_bookings(request):
    """
    Show all bookings of the logged-in patient.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def book_test(request):
    """
    Handle booking form submission from the popup.
    """
    if request.method == 'POST':
        test_id = request.POST.get('test_id')

        test = get_object_or_404(Test, id=test_id)

        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        #  IMPORTANT:
        # Adjust field names here to match your Booking model exactly!
        Booking.objects.create(
            user=request.user,   # or user=request.user if your field is named 'user'
            test=test,
            full_name=full_name,
            age=age,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
        )

        return redirect('my_bookings')

    # if someone tries GET on /book-test/, just send them home
    return redirect('home')
