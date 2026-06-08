let generatedData = null;
let storyName = "";
let generatedTestCases = [];
let currentEditIndex = -1;

async function generateTestCases() {

    const storyName =
        document.getElementById("storyName").value;

    const description =
        document.getElementById("storyDescription").value;

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            story_name: storyName,
            description: description
        })
    });

    const data = await response.json();

    generatedData = data;
    console.log(data);

    displayTestCases(data);
}

function displayTestCases(data) {

    generatedTestCases = [];

    const lines =
        data.raw_response.split("\n");

    let currentType = "";

    let currentTC = null;

    let tcCounter = 1;
    let collectingSteps = false;

    lines.forEach(line => {
        
        line = line.trim();

        if (
            line.includes(
                "Functional Test Cases"
            )
        ) {
            currentType =
                "Functional";
            return;
        }

        if (
            line.includes(
                "Negative Test Cases"
            )
        ) {
            currentType =
                "Negative";
            return;
        }

        if (
            line.includes(
                "Boundary Test Cases"
            )
        ) {
            currentType =
                "Boundary";
            return;
        }

        if (
            line.startsWith("Title:")
        ) {

            if (currentTC) {
                generatedTestCases.push(
                    currentTC
                );
            }

            currentTC = {

                id:
                    `TC-${tcCounter++}`,

                type:
                    currentType,

                title:
                    line.replace(
                        "Title:",
                        ""
                    ).trim(),

                priority: "",

                preconditions: "",

                steps: "",

                expectedResult: ""
            };
        }

        else if (
            line.startsWith(
                "Priority:"
            )
        ) {

            currentTC.priority =
                line.replace(
                    "Priority:",
                    ""
                ).trim();
        }

        else if (
            line.startsWith(
                "Preconditions:"
            )
        ) {

            currentTC.preconditions =
                line.replace(
                    "Preconditions:",
                    ""
                ).trim();
        }

        else if (
            line.startsWith(
                "Steps:"
            )
        ) {

            collectingSteps = true;
            currentTC.steps = "";

        }

        else if (
            line.startsWith(
                "Expected Result:"
            )
        ) {

            collectingSteps = false;
            currentTC.expectedResult =
            line.replace(
                "Expected Result:",
                ""
            ).trim();
        }
        if (
            collectingSteps &&
            !line.startsWith(
                "Expected Result:"
            ) &&
            !line.startsWith(
                "Priority:"
            ) &&
            !line.startsWith(
                "Preconditions:"
            )
        ) {

            currentTC.steps +=
            line + "\n";
        }
    });

    if (currentTC) {

        generatedTestCases.push(
            currentTC
        );
    }

    renderTable();
}

function renderTable() {

    let html = "";

    generatedTestCases.forEach(
        (tc, index) => {

            html += `
            <tr>

                <td>${tc.id}</td>

                <td>${tc.type}</td>

                <td>${tc.title}</td>

                <td>

                    <button
                        class="btn btn-warning btn-sm"
                        onclick="editTestCase(${index})">

                    Edit

                    </button>

                    <button
                        class="btn btn-danger btn-sm ms-2"
                        onclick="deleteTestCase(${index})">

                    Delete

                    </button>

                </td>

            </tr>`;
        }
    );

    document.getElementById(
        "testcaseResults"
    ).innerHTML = html;

    document.getElementById(
        "resultSection"
    ).style.display = "block";
}

function deleteTestCase(index) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this test case?"
        );

    if (!confirmed) {
        return;
    }

    generatedTestCases.splice(
        index,
        1
    );

    renderTable();
}

function editTestCase(index) {

    currentEditIndex = index;

    const tc =
        generatedTestCases[index];

    document.getElementById(
        "editTitle"
    ).value = tc.title;

    document.getElementById(
        "editPriority"
    ).value = tc.priority;

    document.getElementById(
        "editPreconditions"
    ).value = tc.preconditions;

    const formattedSteps =
    tc.steps.replace(
        /(\d+\.)/g,
        "\n$1"
    ).trim();

    document.getElementById(
        "editSteps"
    ).value = formattedSteps;

    document.getElementById(
        "editExpectedResult"
    ).value =
        tc.expectedResult;

    const modal =
        new bootstrap.Modal(
            document.getElementById(
                "editModal"
            )
        );

    modal.show();
}

function saveTestCase() {

    const tc =
        generatedTestCases[
            currentEditIndex
        ];

    tc.title =
        document.getElementById(
            "editTitle"
        ).value;

    tc.priority =
        document.getElementById(
            "editPriority"
        ).value;

    tc.preconditions =
        document.getElementById(
            "editPreconditions"
        ).value;

    tc.steps =
        document.getElementById(
            "editSteps"
        ).value;

    tc.expectedResult =
        document.getElementById(
            "editExpectedResult"
        ).value;

    renderTable();

    bootstrap.Modal
        .getInstance(
            document.getElementById(
                "editModal"
            )
        )
        .hide();
}

async function exportExcel() {

    const storyName =
        document.getElementById("storyName").value;

    const description =
        document.getElementById("storyDescription").value;

    const response = await fetch(
        "/generate-excel",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                story_name: storyName,
                description: description
            })
        }
    );

    const result =
        await response.json();

    alert(result.message);

    console.log(result);
}

async function uploadToZephyr() {

    const response =
        await fetch(
            "/upload-to-zephyr",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        story_name:
                            document.getElementById(
                                "storyName"
                            ).value,

                        test_cases:
                            generatedTestCases
                    }
                )
            }
        );

    const result =
        await response.json();

    console.log(result);

    alert(
        result.message
    );
}