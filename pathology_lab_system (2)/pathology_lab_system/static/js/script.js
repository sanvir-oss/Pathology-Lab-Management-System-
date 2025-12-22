function handleBookClick(testId, testName, testPrice) {
    if (!window.LABXPERT.isAuthenticated) {
        alert("Please login first to book the test.");
        window.location.href = window.LABXPERT.loginUrl;
        return;
    }

    // user is logged in → open your existing modal
    openBookingModal(testId, testName, testPrice);
}







// Open modal and fill values
function openBookingModal(testId, testName, testPrice) {
    document.getElementById('modalTestName').innerText = testName;
    document.getElementById('modalTestPrice').innerText = testPrice;
    document.getElementById('modalTestId').value = testId;

    const modal = document.getElementById('bookingModal');
    modal.style.display = 'block';
}

// Close modal
function closeBookingModal() {
    const modal = document.getElementById('bookingModal');
    modal.style.display = 'none';
}

// Optional: close when clicking outside the modal
window.onclick = function (event) {
    const modal = document.getElementById('bookingModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};
