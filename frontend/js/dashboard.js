
const studentName = localStorage.getItem("student_name");

if (studentName) {
    document.getElementById("welcomeName").innerHTML =
        `👋 Welcome, ${studentName}`;
}async function loadInternships() {

    try {

        const response = await fetch("http://127.0.0.1:8000/recommendations");

        if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
        }

        const internships = await response.json();

        // Update AI Match Score
        if (internships.length > 0) {
            document.getElementById("matchScore").innerHTML =
    internships[0].match_score + "%";
        }

        // Update Resume Status
        const resumeStatus = document.getElementById("resume-status");
        if (resumeStatus) {
            resumeStatus.innerHTML = "✅ Uploaded";
        }

        let html = "";

        internships.forEach(job => {

            html += `
            <div class="border rounded p-3 mb-3">

                <h5>${job.company}</h5>

                <p><strong>${job.role}</strong></p>

                <p>📍 ${job.location}</p>

                <p>💰 ${job.stipend}</p>

                <p style="color:green;font-weight:bold;">
                    ⭐ AI Match: ${job.match_score}%
                </p>

                <button
                    class="btn login-btn w-100"
                    onclick="viewDetails(
                        '${job.company}',
                        '${job.role}',
                        '${job.location}',
                        '${job.stipend}',
                        '${job.match_score}'
                    )">
                    View Details
                </button>

            </div>
            `;

        });

        document.getElementById("internship-list").innerHTML = html;

    } catch (error) {

        console.error("Error:", error);

        document.getElementById("internship-list").innerHTML =
            "<p style='color:red;'>Failed to load internships.</p>";

    }

}

function viewDetails(company, role, location, stipend, match) {

    const url =
        `job-details.html?company=${encodeURIComponent(company)}` +
        `&role=${encodeURIComponent(role)}` +
        `&location=${encodeURIComponent(location)}` +
        `&stipend=${encodeURIComponent(stipend)}` +
        `&match=${encodeURIComponent(match)}`;

    window.location.href = url;

}

loadInternships();