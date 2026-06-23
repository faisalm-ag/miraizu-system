document.addEventListener('DOMContentLoaded', function () {
    
    // =============================================================
    // 1. QUESTIONNAIRE FORM VALIDATION
    // =============================================================
    const kuesionerForm = document.querySelector('form[action="/kuesioner"]');
    
    if (kuesionerForm) {
        kuesionerForm.addEventListener('submit', function (event) {
            let allChecked = true;
            let missingQuestions = [];

            for (let i = 1; i <= 12; i++) {
                const questionRadio = document.getElementsByName(`q${i}`);
                let isChecked = false;

                for (let j = 0; j < questionRadio.length; j++) {
                    if (questionRadio[j].checked) {
                        isChecked = true;
                        break;
                    }
                }

                if (!isChecked) {
                    allChecked = false;
                    missingQuestions.push(i);
                }
            }

            if (!allChecked) {
                event.preventDefault();
                alert(`Pengisian instrumen kuesioner belum lengkap.\nSilakan lengkapi butir pertanyaan nomor: ${missingQuestions.join(', ')}`);
            }
        });
    }

    // =============================================================
    // 2. RESET SESSION CONFIRMATION
    // =============================================================
    const btnReset = document.querySelector('a[href="/reset"]');
    
    if (btnReset) {
        btnReset.addEventListener('click', function (event) {
            const confirmReset = confirm("Apakah Anda yakin ingin melakukan restorasi sistem? Tindakan ini akan menghapus seluruh data profil dan hasil sintesis pengujian.");
            if (!confirmReset) {
                event.preventDefault();
            }
        });
    }

    // =============================================================
    // 3. FLASH MESSAGES AUTO-FADE DISMISSAL
    // =============================================================
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(function () {
            flashMessages.forEach(function (alert) {
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";
                setTimeout(function () {
                    alert.remove();
                }, 500);
            });
        }, 4000);
    }
});