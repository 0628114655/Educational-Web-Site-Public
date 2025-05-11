document.addEventListener('DOMContentLoaded', function() {
    const lockFields = document.querySelectorAll('.lock-field');
    const unlockButton = document.getElementById('unlock-button');

    if (unlockButton) {
        unlockButton.addEventListener('click', function() {
            lockFields.forEach(function(field) {
                field.disabled = false;
            });
            unlockButton.style.display = 'none';
        });
    }
})