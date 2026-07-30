const params = new URLSearchParams(window.location.search);

document.getElementById("company").innerHTML =
params.get("company");

document.getElementById("role").innerHTML =
params.get("role");

document.getElementById("location").innerHTML =
"📍 " + params.get("location");

document.getElementById("stipend").innerHTML =
"💰 " + params.get("stipend");

document.getElementById("match").innerHTML =
"⭐ AI Match: " + params.get("match") + "%";

async function applyInternship() {

    const application = {
        company: params.get("company"),
        role: params.get("role")
    };

    try {

        const response = await fetch("http://127.0.0.1:8000/apply", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(application)

        });

        const result = await response.json();

        alert(result.message);

        window.location.href = "dashboard.html";

    } catch (error) {

        console.error(error);

        alert("Failed to submit application!");

    }

}