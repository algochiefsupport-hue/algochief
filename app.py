<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Report Tracker</title>
    <!-- Tailwind CSS for clean look -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <!-- ApexCharts for professional zoom & scroll charts -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
</head>
<body class="bg-gray-50 text-gray-800 font-sans">

    <!-- Top Navigation Bar -->
    <header class="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-between shadow-xs">
        <h1 class="text-xl font-bold text-blue-600 flex items-center gap-2">
            📊 Medical Report Health Tracker
        </h1>
        <div>
            <label class="cursor-pointer bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition flex items-center gap-2">
                📁 Upload Report (PDF/Photo)
                <input type="file" id="fileUpload" accept="image/*,.pdf" class="hidden" onchange="handleFileUpload(event)">
            </label>
        </div>
    </header>

    <div class="flex h-[calc(100vh-73px)] overflow-hidden">
        
        <!-- Left Sidebar: Test Selection List -->
        <aside class="w-1/4 bg-white border-r border-gray-200 p-4 overflow-y-auto">
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">All Tests</h2>
            <div id="testList" class="space-y-1">
                <!-- JavaScript handles items here -->
            </div>
        </aside>

        <!-- Right Main Panel: Normal Range & Big Zoomable Chart -->
        <main class="w-3/4 p-6 overflow-y-auto bg-gray-50">
            <!-- Test Title & Ranges -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-xs mb-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 id="activeTestName" class="text-2xl font-bold text-gray-900">Select a Test</h2>
                </div>
                
                <!-- Range Cards -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-emerald-50 border border-emerald-100 p-4 rounded-lg">
                        <span class="text-xs font-semibold text-emerald-700 uppercase block">Kitna Rehna Chahiye (Minimum Normal)</span>
                        <span id="minNormal" class="text-xl font-bold text-emerald-900">--</span>
                    </div>
                    <div class="bg-rose-50 border border-rose-100 p-4 rounded-lg">
                        <span class="text-xs font-semibold text-rose-700 uppercase block">Kitna Rehna Chahiye (Maximum Normal)</span>
                        <span id="maxNormal" class="text-xl font-bold text-rose-900">--</span>
                    </div>
                </div>
            </div>

            <!-- Big Interactive Chart Container -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-xs">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs text-gray-400 font-medium">💡 Tip: Chart ko click karke aage-piche (drag) karein ya zoom karein</span>
                </div>
                <div id="chartContainer" class="w-full h-[400px]">
                    <!-- ApexCharts rendering here -->
                </div>
            </div>
        </main>
    </div>

    <script>
        // Default Sample Data (Initial State)
        let medicalData = {
            "24 Hours Urine Protein": {
                minRange: "0 mg/day",
                maxRange: "150 mg/day",
                history: [
                    { date: "2026-01-10", value: 120 },
                    { date: "2026-02-15", value: 180 },
                    { date: "2026-03-20", value: 140 },
                    { date: "2026-04-25", value: 160 },
                    { date: "2026-05-30", value: 110 }
                ]
            },
            "SGPT (ALT)": {
                minRange: "7 U/L",
                maxRange: "56 U/L",
                history: [
                    { date: "2026-01-10", value: 42 },
                    { date: "2026-02-15", value: 65 },
                    { date: "2026-03-20", value: 50 },
                    { date: "2026-04-25", value: 72 },
                    { date: "2026-05-30", value: 48 }
                ]
            },
            "SGOT (AST)": {
                minRange: "10 U/L",
                maxRange: "40 U/L",
                history: [
                    { date: "2026-01-10", value: 35 },
                    { date: "2026-02-15", value: 48 },
                    { date: "2026-03-20", value: 39 },
                    { date: "2026-04-25", value: 55 },
                    { date: "2026-05-30", value: 37 }
                ]
            }
        };

        let activeTest = "24 Hours Urine Protein";
        let chartInstance = null;

        // Render the Sidebar List
        function renderSidebar() {
            const listContainer = document.getElementById("testList");
            listContainer.innerHTML = "";
            
            Object.keys(medicalData).forEach(testName => {
                const isSelected = testName === activeTest;
                const button = document.createElement("button");
                button.className = `w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition ${
                    isSelected 
                    ? "bg-blue-50 text-blue-700 border-l-4 border-blue-600 pl-3" 
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                }`;
                button.textContent = testName;
                button.onclick = () => selectTest(testName);
                listContainer.appendChild(button);
            });
        }

        // Handle Test Selection Click
        function selectTest(testName) {
            activeTest = testName;
            renderSidebar();
            updateDashboardView();
        }

        // Update Dashboard Data and Refresh Interactive Chart
        function updateDashboardView() {
            const testInfo = medicalData[activeTest];
            document.getElementById("activeTestName").textContent = activeTest;
            document.getElementById("minNormal").textContent = testInfo.minRange;
            document.getElementById("maxNormal").textContent = testInfo.maxRange;

            // Sort history data chronologically by date
            const sortedHistory = [...testInfo.history].sort((a, b) => new Date(a.date) - new Date(b.date));
            const categories = sortedHistory.map(item => item.date);
            const dataValues = sortedHistory.map(item => item.value);

            // Chart Configuration options for Zooming and Panning
            const options = {
                series: [{
                    name: activeTest,
                    data: dataValues
                }],
                chart: {
                    type: 'line',
                    height: 380,
                    zoom: {
                        enabled: true,
                        type: 'x',
                        autoScaleYaxis: true
                    },
                    toolbar: {
                        autoSelected: 'zoom',
                        tools: {
                            download: false,
                            selection: true,
                            zoom: true,
                            zoomin: true,
                            zoomout: true,
                            pan: true,
                            reset: true
                        }
                    }
                },
                colors: ['#2563eb'],
                dataLabels: { enabled: true },
                stroke: { curve: 'smooth', width: 3 },
                grid: { borderColor: '#e2e8f0' },
                xaxis: {
                    categories: categories,
                    title: { text: 'Report Dates' }
                },
                yaxis: {
                    title: { text: 'Value' }
                }
            };

            // Destroy older instance to prevent memory leaks or overlapping text
            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new ApexCharts(document.querySelector("#chartContainer"), options);
            chartInstance.render();
        }

        // Simulated Automatic Report Data Extraction on File Upload
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Simple loading simulation alert
            alert("File upload successful! System text AI tests detect kar raha hai...");

            setTimeout(() => {
                // Mimicking auto-detection of a new date and values for the tests
                const randomDay = Math.floor(Math.random() * 28) + 1;
                const formattedDay = randomDay < 10 ? '0' + randomDay : randomDay;
                const newDate = `2026-06-${formattedDay}`;

                // Adding values automatically to existing tests
                medicalData["24 Hours Urine Protein"].history.push({ date: newDate, value: Math.floor(Math.random() * 100) + 100 });
                medicalData["SGPT (ALT)"].history.push({ date: newDate, value: Math.floor(Math.random() * 40) + 35 });
                medicalData["SGOT (AST)"].history.push({ date: newDate, value: Math.floor(Math.random() * 30) + 25 });

                alert("Nayi report ka data auto detect hokar saare charts me add ho gaya hai!");
                updateDashboardView();
            }, 1000);
        }

        // Initialize App on Startup
        window.onload = () => {
            renderSidebar();
            updateDashboardView();
        };
    </script>
</body>
</html>
