async function loadApplications() {

    try {

        const response = await fetch("http://127.0.0.1:8000/applications");

if (!response.ok) {
    throw new Error("Failed to load applications");
}

const applications = await response.json();

        let html = "";

        if (applications.length === 0) {

            html = "<p>No applications found.</p>";

        } else {

            applications.forEach(app => {

                html += `
                <div class="border rounded p-3 mb-3">

                    <h5>${app.company}</h5>

                    <p>${app.role}</p>

                    <p style="color:green;font-weight:bold;">
                        ✅ Applied
                    </p>

                </div>
                `;

            });

        }

        document.getElementById("applications-list").innerHTML = html;

    } catch (error) {

        console.error(error);

        document.getElementById("applications-list").innerHTML =
            "<p style='color:red;'>Failed to load applications.</p>";

    }

}

loadApplications();