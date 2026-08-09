async function registerStudent() {

    const student = {

        full_name: document.getElementById("full_name").value,
        email: document.getElementById("email").value,
        college: document.getElementById("college").value,
        degree: document.getElementById("degree").value,
        skills: document.getElementById("skills").value

    };

    try {

        const response = await fetch("https://smartintern-ai11-1.onrender.com/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(student)

        });

        const result = await response.json();

        alert(result.message);

        if (response.ok) {
            localStorage.setItem("student_email", student.email);
            localStorage.setItem("student_name", student.full_name);

            window.location.href = "dashboard.html";
        }

    } catch (error) {

        console.error(error);
        alert("Cannot connect to backend.");

    }

}