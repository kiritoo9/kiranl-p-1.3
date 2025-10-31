<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digi Mini-BI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/2.0.8/css/dataTables.dataTables.css">

    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/xy.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/percent.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/numeral.js/2.0.6/numeral.min.js"></script>

    <style>
        html {
            font-family: 'Inter', sans-serif;
        }

        #data-table_wrapper .dt-paging .dt-paging-button:not(.current):not(:hover) {
            background: white;
            color: #3b82f6;
            border-color: #bfdbfe;
        }

        #data-table_wrapper .dt-paging .dt-paging-button:hover {
            background: #eff6ff;
            color: #2563eb;
            border-color: #bfdbfe;
        }

        #data-table_wrapper .dt-paging .dt-paging-button.current,
        #data-table_wrapper .dt-paging .dt-paging-button.current:hover {
            background: #3b82f6 !important;
            color: white !important;
            border-color: #3b82f6 !important;
        }

        #data-table_wrapper .dt-length select {
            padding: 0.5rem 2rem 0.5rem 0.75rem;
            border: 1px solid #bfdbfe;
            border-radius: 0.375rem;
        }

        #data-table tbody tr {
            color: #1f2937;
            border-bottom: 1px solid #bfdbfe;
        }

        #data-table tbody tr:last-child {
            border-bottom: none;
        }

        #data-table tbody tr:hover {
            background-color: #f9fafb;
        }

        #data-table_wrapper .dt-info {
            font-size: 0.875rem;
            color: #6b7280;
        }

        #data-table thead th,
        #data-table tbody td {
            padding: 0.5rem 1rem;
            font-size: 13px;
        }
    </style>
</head>

<body class="font-sans antialiased text-gray-900">

    <div id="welcome-screen" class="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
        <img src="./digi512x512.png" style="width: 100px; height: 100px; object-fit: contain; margin-bottom: 25px;" />
        <p class="text-gray-600 mb-8 text-center text-base">Your best technology partner.</p>

        <div class="w-full max-w-lg flex shadow rounded-full">
            <input type="text" id="initial-prompt" placeholder="Buatkan laporan tagihan air tahun 2022"
                class="flex-1 px-5 py-3 border-y border-l border-gray-300 rounded-l-full focus:outline-none focus:ring-2 focus:ring-blue-100 text-base">
            <button id="start-btn"
                class="bg-blue-500 text-white px-8 py-3 rounded-r-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-base">
                Kirim
            </button>
        </div>
    </div>


    <div id="main-app" class="flex h-screen overflow-hidden bg-gray-100 hidden">

        <div class="flex flex-col h-full w-1/3 bg-white border-r border-gray-200">
            <div class="px-4 py-2 border-b border-gray-200 shadow-sm">
                <h2 class="text-xl font-semibold text-gray-800">
                    <img src="./digi512x512.png" style="width: 50px; height: 50px; object-fit: contain;" />
                </h2>
            </div>
            <div id="chat-history" class="flex-1 overflow-y-auto p-6 space-y-4"></div>
            <div class="p-4 bg-gray-50 border-t border-gray-200">
                <div class="flex space-x-3">
                    <input type="text" id="chat-input" placeholder="Buat laporan baru.."
                        class="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                    <button id="send-btn"
                        class="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow text-sm font-medium">
                        Kirim
                    </button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex flex-col h-full bg-gray-50 overflow-hidden">

            <div class="p-4 bg-white border-b border-gray-200 shadow-sm">
                <div class="flex justify-between items-center">
                    <h2 class="text-xl font-semibold text-gray-800">Visualisasi Data</h2>
                    <div id="btn-action" class="flex items-center space-x-4" style="display: none;">
                        <div>
                            <select id="report-switcher"
                                class="border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm">
                                <option value="table" selected>Table</option>
                                <option value="bar">Bar Chart</option>
                                <option value="line">Line Chart</option>
                                <option value="pie">Pie Chart</option>
                            </select>
                        </div>
                        <button id="filter-btn"
                            class="flex items-center space-x-2 bg-white border border-gray-300 rounded-md shadow-sm py-2 px-4 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                            </svg>
                            <span>Filter</span>
                        </button>
                    </div>
                </div>
            </div>

            <div class="flex-1 p-6 overflow-hidden relative">

                <div id="chart-loader"
                    class="absolute inset-6 z-10 flex items-center justify-center bg-white bg-opacity-75 rounded-lg hidden">
                    <i class="fas fa-spinner fa-spin fa-3x text-blue-500"></i>
                </div>

                <div id="no-context" class="w-full h-full bg-white rounded-lg shadow-inner p-4 flex items-center justify-center text-center" style="display: none;">
                    <img src="./not-found.jpg" class="max-w-full max-h-full object-contain" />
                </div>

                <div id="chart-container" class="w-full h-full bg-white rounded-lg shadow-inner p-4"></div>

                <div id="table-container" class="w-full h-full hidden overflow-hidden bg-white rounded-lg shadow-inner">
                    <div class="w-full h-full overflow-auto p-4">
                        <table id="data-table" class="display" style="width:100%">
                            <thead id="table-header"></thead>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="filter-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 hidden">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="text-lg font-semibold">Filter Data</h3>
                <button id="close-modal-btn" class="text-gray-400 hover:text-gray-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="p-6 space-y-4" id="box-filters">
                <div style="display: hidden;">
                    <label for="filter-range-date" class="block text-sm font-medium text-gray-700">Rentang
                        Tanggal</label>
                    <input type="text" id="filter-range-date" placeholder="Pilih rentang tanggal..."
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                </div>

                <div>
                    <label for="filter-text-produk" class="block text-sm font-medium text-gray-700">Nama Produk
                        (contains)</label>
                    <input type="text" id="filter-text-produk" placeholder="Contoh: 'Laptop'"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                </div>
            </div>
            <div class="flex justify-end space-x-3 p-4 bg-gray-50 border-t rounded-b-lg">
                <button id="apply-filter-btn"
                    class="bg-blue-500 text-white rounded-md shadow-sm py-2 px-4 text-sm font-medium hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    Terapkan
                </button>
            </div>
        </div>
    </div>


    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
    <script src="https://npmcdn.com/flatpickr/dist/l10n/id.js"></script>

    <script>
        const HOST = "http://0.0.0.0:5000";
        const API_KEY = "CCHjCcW7D9Arw5qJEFpxNd3";

        // backend global-var
        var FILTERS = [];
        var TABLE_PARAMS = {
            page: 1,
            size: 10,
            total_page: 1
        };
        var TABLE_FILTERS = {
            "id": null,
            "filters": [],
            "order_by": null,
            "page": 1,
            "size": 10
        }

        var FILTER_APPENDED = [];

        // UI global-var
        var am5Root;
        var currentChart;
        var currentDataTable;
        var pieData, barData, lineData, tableData;
        var appInitialized = false;
        var tableInitialized = false;
        const ERR_MSG = {
            NO_CONTEXT: 'Maaf aku tidak mengenali permintaanmu :( \n\nApakah kamu salah mengetikan sesuatu?'
        }

        function handleSendChat() {
            $('#no-context').hide();
            const message = $('#chat-input').val().trim();
            if (message === "") return;
            addChatMessage(message, 'user');
            $('#chat-input').val('');
            showTypingIndicator();
            $('#chart-loader').removeClass('hidden');
            getBotResponse(message);
        }

        function addChatMessage(message, sender) {
            let bubbleHtml = '';
            if (sender === 'user') {
                bubbleHtml = `
                <div class="flex justify-end">
                    <div class="bg-blue-500 text-white rounded-lg p-3 max-w-xs shadow">
                        <p>${message}</p>
                    </div>
                </div>`;
            } else {
                bubbleHtml = `
                <div class="flex justify-start">
                    <div class="bg-gray-200 text-gray-800 rounded-lg p-3 max-w-xs shadow">
                        <p>${message}</p>
                    </div>
                </div>`;
            }
            $('#chat-history').append(bubbleHtml);
            $('#chat-history').scrollTop($('#chat-history')[0].scrollHeight);
        }

        function showTypingIndicator() {
            const typingHtml = `
                <div id="typing-bubble" class="flex justify-start">
                    <div class="bg-gray-200 text-gray-800 rounded-lg p-3 max-w-xs shadow">
                        <div class="typing-indicator"><i>Thinking..</i></div>
                    </div>
                </div>`;
            $('#chat-history').append(typingHtml);
            $('#chat-history').scrollTop($('#chat-history')[0].scrollHeight);
        }

        function generateFilter(f) {
            const type = f?.type?.toUpperCase();
            let name = f?.name ?? '-';
            const id = `filter-${name}`;
            const label = name.replace(/_/g, ' ');

            if (type === "DATE") {
                const _html = `<div>
                        <label for="${id}" class="block text-sm font-medium text-gray-700" style="text-transform: capitalize">${label}</label>
                        <input type="text" id="${id}" placeholder="Pilih tanggal..." class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                    </div>`;

                // append and inject library
                $("#box-filters").append(_html);
                flatpickr(`#${id}`, {
                    mode: "range",
                    dateFormat: "Y-m-d"
                });
                FILTER_APPENDED.push({
                    name: name,
                    operator: "BETWEEN",
                    value: null,
                    type: f.type.toUpperCase(),
                    el: id
                });
            } else if (["BIGINT", "INT"].includes(type)) {
                let _options = '';
                for (const o of ['=', '>', '<', '>=', '<=']) {
                    _options += `<option value="${o}">${o}</option>`;
                }

                const _html = `
                    <div class="flex items-center gap-4">
                        <div class="w-1/4">
                            <label for="${id}-operator" class="block text-sm font-medium text-gray-700" style="text-transform: capitalize">
                                Operator
                            </label>
                            <select id="${id}-operator" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">${_options}</select>
                        </div>

                        <div class="flex-1">
                            <label for="${id}-val" class="block text-sm font-medium text-gray-700" style="text-transform: capitalize">
                                ${label}
                            </label>
                            <input type="number" id="${id}-val" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        </div>
                    </div>
                `;

                // append and inject library
                $("#box-filters").append(_html);
                FILTER_APPENDED.push({
                    name: name,
                    operator: null,
                    value: null,
                    type: f.type.toUpperCase(),
                    el: id
                });
            }

            return null;
        }

        function getBotResponse(userMessage) {
            $.ajax({
                url: `${HOST}/generate_report`,
                type: 'POST',
                data: JSON.stringify({
                    prompt: userMessage
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${API_KEY}`
                },
                success: function(response) {
                    $('#no-context').hide();
                    $('#typing-bubble').remove();

                    // preparing output
                    let greetingMsg = "";
                    let closingMsg = "";
                    const rows = response?.data?.rows ?? [];
                    TABLE_FILTERS.id = response?.data?.id ?? null;

                    if (response?.data?.parameters !== undefined) {
                        TABLE_PARAMS = {
                            page: response?.data?.parameters?.page ?? TABLE_PARAMS.page,
                            size: response?.data?.parameters?.size ?? TABLE_PARAMS.size,
                            total_page: response?.data?.parameters?.total_page ?? TABLE_PARAMS.total_page,
                        }
                    }

                    if (response?.sentences?.greeting !== undefined) greetingMsg = response.sentences.greeting;
                    if (response?.sentences?.closing !== undefined) closingMsg = response.sentences.closing;

                    if (TABLE_FILTERS.id && greetingMsg && closingMsg && rows.length > 0) {
                        addChatMessage(greetingMsg, 'bot');
                        showTypingIndicator();

                        // generating filters
                        const baseFilters = response?.data?.filters ?? [];
                        $("#box-filters").html(''); // clean filters
                        for (const f of baseFilters) generateFilter(f);

                        // populating data
                        tableData = rows;
                        setTimeout(() => {
                            // hide loading
                            $('#chart-loader').addClass('hidden');
                            $('#typing-bubble').remove();

                            // showing report
                            $('#btn-action').show();
                            addChatMessage(closingMsg, 'bot');
                            showReport('table');
                        }, 500);
                    } else {
                        throw new Error();
                    }
                },
                error: function(xhr, status, error) {
                    // hiding elements
                    $('#chart-loader').addClass('hidden');
                    $('#typing-bubble').remove();
                    $('#chart-container').hide();
                    $('#table-container').hide();
                    $('#btn-action').hide();
                    $('#no-context').show();

                    // show message as bot
                    addChatMessage(ERR_MSG.NO_CONTEXT, 'bot');
                },
            });
        }

        function showReport(type) {
            if (type === 'table') {
                $('#chart-container').hide();
                $('#table-container').show();
                initializeDataTable();
            } else {
                $('#table-container').hide();
                $('#chart-container').show();

                if (currentChart) {
                    currentChart.dispose();
                }

                if (type === 'pie') {
                    currentChart = createPieChart(pieData);
                } else if (type === 'bar') {
                    currentChart = createBarChart(barData);
                } else if (type === 'line') {
                    currentChart = createLineChart(lineData);
                }
            }
        }

        function updateDashboard() {
            const currentType = $('#report-switcher').val();
            if (currentType === 'table') {
                if (currentDataTable) {
                    currentDataTable.ajax.reload(null, false);
                } else {
                    initializeDataTable();
                }
            } else {
                showReport(currentType);
            }
        }

        function formatValue(value) {
            if (Number.isInteger(value)) {
                return numeral(value).format('0,0');
            }
            return value;
        }

        function initializeDataTable() {
            if (currentDataTable) currentDataTable.destroy();

            let columns = [];
            if (!tableData) {
                tableData = [];
            } else if (tableData.length > 0) {
                // extract columns
                const col = tableData[0];
                let theadHtml = '<tr>';

                for (let i = 0; i < Object.keys(col).length; i++) {
                    const t = Object.keys(col)[i];
                    const tclean = t.replace(/_/g, ' ');

                    columns.push({
                        data: t,
                        title: tclean
                    });
                    theadHtml += `<th class="text-left text-xs font-bold text-blue-700 uppercase tracking-wider" style="font-size:capitalize">${tclean}</th>`;
                }
                $("#table-header").html(theadHtml);
            }

            currentDataTable = $('#data-table').DataTable({
                processing: true,
                serverSide: true,
                searching: false,
                ajax: function(data, callback, settings) {

                    if (tableInitialized) {
                        // check order by
                        if (data?.order !== undefined && data.order.length > 0) {
                            const orDir = data.order[0]?.dir ?? 'asc';
                            const orCol = data.order[0]?.column ?? -1;
                            if (orCol >= 0) {
                                const col = data.columns[orCol]?.data;
                                if (col) TABLE_FILTERS.order_by = `${col} ${orDir}`;
                            }
                        }

                        // check paging
                        TABLE_FILTERS.size = data.length;
                        TABLE_FILTERS.page = Math.floor(data.start / data.length) + 1;

                        // update global-var for table filters
                        $.ajax({
                            url: `${HOST}/change_context`,
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${API_KEY}`
                            },
                            contentType: 'application/json',
                            data: JSON.stringify(TABLE_FILTERS),
                            success: function(resp) {
                                const params = resp?.parameters ?? null;
                                if (!params) throw new Error();

                                const rows = resp.rows;
                                const totalRecords = params.total_page * params.size;

                                // update rows
                                $('#chart-loader').addClass('hidden');
                                callback({
                                    draw: data.draw,
                                    recordsTotal: totalRecords,
                                    recordsFiltered: totalRecords,
                                    data: rows
                                });
                            },
                            error: function(xhr) {
                                $('#chart-loader').addClass('hidden');
                                addChatMessage(ERR_MSG.NO_CONTEXT, 'bot');
                                callback({
                                    draw: data.draw,
                                    recordsTotal: 0,
                                    recordsFiltered: 0,
                                    data: []
                                });
                            }
                        });
                    }

                    const totalRecords = TABLE_PARAMS.total_page * TABLE_PARAMS.size;
                    tableInitialized = true;
                    callback({
                        draw: data.draw,
                        recordsTotal: totalRecords,
                        recordsFiltered: totalRecords,
                        data: tableData
                    });
                },
                columns: columns.map(col => ({
                    data: col.data,
                    title: col.title,
                    createdCell: function(td, cellData, rowData, row, col) {
                        $(td).removeClass('dt-right').addClass('text-left');
                    },
                    render: (value) => formatValue(value)
                })),
            });
        }

        function createPieChart(data) {
            let chart = am5Root.container.children.push(
                am5percent.PieChart.new(am5Root, {
                    layout: am5Root.verticalLayout,
                    innerRadius: am5.percent(50)
                })
            );

            let series = chart.series.push(
                am5percent.PieSeries.new(am5Root, {
                    valueField: "value",
                    categoryField: "category",
                    alignLabels: false
                })
            );

            series.labels.template.setAll({
                textType: "circular",
                centerX: 0,
                centerY: 0,
                fill: am5.color(0x333333),
                fontSize: 15
            });

            series.ticks.template.set("forceHidden", true);
            series.data.setAll(data);
            series.appear(1000, 100);

            let legend = chart.children.push(am5.Legend.new(am5Root, {
                centerX: am5.percent(50),
                x: am5.percent(50),
                marginTop: 15,
                marginBottom: 15
            }));
            legend.data.setAll(series.dataItems);

            return chart;
        }

        function createBarChart(data) {
            let chart = am5Root.container.children.push(
                am5xy.XYChart.new(am5Root, {
                    panX: false,
                    panY: false,
                    wheelX: "none",
                    wheelY: "none"
                })
            );

            let xAxis = chart.xAxes.push(
                am5xy.CategoryAxis.new(am5Root, {
                    categoryField: "category",
                    renderer: am5xy.AxisRendererX.new(am5Root, {
                        minGridDistance: 20
                    }),
                    tooltip: am5.Tooltip.new(am5Root, {})
                })
            );
            xAxis.data.setAll(data);

            let yAxis = chart.yAxes.push(
                am5xy.ValueAxis.new(am5Root, {
                    renderer: am5xy.AxisRendererY.new(am5Root, {}),
                    min: 0
                })
            );

            let series = chart.series.push(
                am5xy.ColumnSeries.new(am5Root, {
                    name: "Sales",
                    xAxis: xAxis,
                    yAxis: yAxis,
                    valueYField: "sales",
                    categoryXField: "category",
                    sequencedInterpolation: true,
                    tooltip: am5.Tooltip.new(am5Root, {
                        pointerOrientation: "vertical",
                        labelText: "[bold]{categoryX}:[/] {valueY}"
                    })
                })
            );

            series.columns.template.setAll({
                cornerRadiusTL: 5,
                cornerRadiusTR: 5,
                strokeOpacity: 0,
                fontSize: 15
            });

            series.data.setAll(data);
            series.appear();
            chart.appear(1000, 100);
            return chart;
        }

        function createLineChart(data) {
            let chart = am5Root.container.children.push(
                am5xy.XYChart.new(am5Root, {
                    panX: true,
                    panY: true,
                    wheelX: "panX",
                    wheelY: "zoomX",
                    pinchZoomX: true
                })
            );

            let xAxis = chart.xAxes.push(
                am5xy.CategoryAxis.new(am5Root, {
                    categoryField: "month",
                    renderer: am5xy.AxisRendererX.new(am5Root, {}),
                    tooltip: am5.Tooltip.new(am5Root, {})
                })
            );
            xAxis.data.setAll(data);

            let yAxis = chart.yAxes.push(
                am5xy.ValueAxis.new(am5Root, {
                    renderer: am5xy.AxisRendererY.new(am5Root, {})
                })
            );

            let series = chart.series.push(
                am5xy.LineSeries.new(am5Root, {
                    name: "Sales",
                    xAxis: xAxis,
                    yAxis: yAxis,
                    valueYField: "sales",
                    categoryXField: "month",
                    tooltip: am5.Tooltip.new(am5Root, {
                        labelText: "{valueY}"
                    })
                })
            );

            series.strokes.template.setAll({
                strokeWidth: 2,
                fontSize: 15
            });

            series.bullets.push(function() {
                return am5.Bullet.new(am5Root, {
                    sprite: am5.Circle.new(am5Root, {
                        radius: 4,
                        fill: series.get("fill"),
                        stroke: am5Root.interfaceColors.get("background"),
                        strokeWidth: 2
                    })
                });
            });

            series.data.setAll(data);
            series.appear(1000);
            chart.appear(1000, 100);
            return chart;
        }

        function initializeMainApp(initialPrompt = "") {
            if (appInitialized) return;
            appInitialized = true;

            $('#welcome-screen').hide();
            $('#main-app').removeClass('hidden').show();

            am5.ready(function() {
                am5Root = am5.Root.new("chart-container");
                am5Root.setThemes([
                    am5themes_Animated.new(am5Root)
                ]);
                am5Root.autoDispose = true;
                if (am5Root._logo) {
                    am5Root._logo.dispose();
                }

                if (initialPrompt.trim() !== "") {
                    addChatMessage(initialPrompt, 'user');
                    showTypingIndicator();
                    $('#chart-loader').removeClass('hidden');
                    getBotResponse(initialPrompt);
                }

            });
        }

        $(document).ready(function() {
            $('#start-btn').on('click', function() {
                const initialPrompt = $('#initial-prompt').val();
                initializeMainApp(initialPrompt);
            });
            $('#initial-prompt').on('keypress', function(e) {
                if (e.which === 13) {
                    $('#start-btn').click();
                }
            });

            $('#send-btn').on('click', handleSendChat);
            $('#chat-input').on('keypress', function(e) {
                if (e.which === 13) {
                    handleSendChat();
                }
            });

            $('#report-switcher').on('change', function() {
                const selectedType = $(this).val();
                showReport(selectedType);
            });

            $('#filter-btn').on('click', function() {
                $('#filter-modal').removeClass('hidden');
            });

            $('#close-modal-btn, #cancel-filter-btn').on('click', function() {
                $('#filter-modal').addClass('hidden');
            });

            $('#apply-filter-btn').on('click', function() {
                // clean filters
                TABLE_FILTERS.filters = [];

                for (const f of FILTER_APPENDED) {
                    const val = $(`#${f?.el}`).val();
                    const type = f?.type ?? '-';

                    if (f?.type === "DATE") {
                        const arrVal = val.split(" - ");
                        if (arrVal.length >= 2) {
                            TABLE_FILTERS.filters.push({
                                name: f.name,
                                operator: f.operator,
                                value: [arrVal[0].trim(), arrVal[1].trim()]
                            });
                        }
                    } else if (['BIGINT', 'INT'].includes(type)) {
                        const op = $(`#${f?.el}-operator`).val();
                        const val = $(`#${f?.el}-val`).val();
                        if (op && val) {
                            TABLE_FILTERS.filters.push({
                                name: f.name,
                                operator: op,
                                value: parseInt(val)
                            });
                        }
                    }
                }

                // re-generate table
                $('#filter-modal').addClass('hidden');
                $('#chart-loader').removeClass('hidden');
                setTimeout(() => {
                    currentDataTable.ajax.reload(null, true);
                }, 1000);
            });

            // init library for date
            flatpickr.localize(flatpickr.l10ns.id);
        });
    </script>
</body>

</html>