<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>每日打卡</title>
  <!-- Tailwind CSS v3 -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Font Awesome -->
  <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
  <!-- 统一的 Tailwind 配置 -->
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#3b82f6',
            secondary: '#10b981',
            accent: '#f59e0b',
            dark: '#1e293b',
            light: '#f8fafc'
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
          },
          animation: {
            'bounce-short': 'bounce 0.5s ease-in-out',
            'pulse-short': 'pulse 0.5s ease-in-out',
          }
        }
      }
    }
  </script>
  <style type="text/tailwindcss">
    @layer utilities {
      .content-auto {
        content-visibility: auto;
      }
      .text-shadow {
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      .card-shadow {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      }
      .calendar-day {
        aspect-ratio: 1/1;
        transition: all 0.2s ease;
        cursor: pointer;
      }
      .calendar-day:hover {
        background-color: rgba(59, 130, 246, 0.1);
      }
      .calendar-day-completed {
        background-color: theme('colors.primary');
        color: white;
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
      }
      .calendar-day-completed:hover {
        background-color: theme('colors.primary');
        transform: scale(1.05);
      }
      .calendar-day-today {
        border: 2px solid theme('colors.primary');
        font-weight: bold;
      }
      .calendar-day-other-month {
        color: #e5e7eb;
      }
      .calendar-legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-right: 16px;
      }
      .calendar-legend-color {
        width: 16px;
        height: 16px;
        border-radius: 50%;
      }
      .achievement-badge {
        transition: transform 0.3s ease;
      }
      .achievement-badge:hover {
        transform: scale(1.1);
      }
      .checkin-button {
        transition: all 0.3s ease;
      }
      .checkin-button:active {
        transform: scale(0.95);
      }
      .checkin-button.completed {
        background-color: theme('colors.secondary');
        animation: pulse 2s infinite;
      }
      .habit-card {
        transition: all 0.3s ease;
      }
      .habit-card:hover {
        transform: translateY(-5px);
      }
      .habit-card.active {
        border-color: theme('colors.primary');
        border-width: 2px;
      }
    }
  </style>
</head>
<body class="bg-gray-50 min-h-screen">
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- 顶部导航 -->
    <header class="mb-8">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-dark text-shadow">每日打卡</h1>
        <button id="add-habit-btn" class="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-600 transition-colors">
          <i class="fa fa-plus"></i>
          <span>添加目标打卡</span>
        </button>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main>
      <!-- 习惯选择区域 -->
      <section class="mb-8">
        <div class="flex overflow-x-auto pb-4 gap-4" id="habits-container">
          <!-- 习惯卡片将通过 JavaScript 动态生成 -->
        </div>
      </section>

      <!-- 当前习惯详情 -->
      <section id="habit-details" class="mb-8 hidden">
        <div class="bg-white rounded-xl p-6 card-shadow">
          <div class="flex justify-between items-center mb-6">
            <div class="flex items-center gap-3">
              <div id="habit-icon" class="w-12 h-12 rounded-full flex items-center justify-center text-white text-2xl"></div>
              <div>
                <h2 id="habit-name" class="text-2xl font-bold text-dark"></h2>
                <p id="habit-streak" class="text-gray-500"></p>
              </div>
            </div>
            <button id="edit-habit-btn" class="text-gray-500 hover:text-primary">
              <i class="fa fa-pencil text-xl"></i>
            </button>
          </div>

          <!-- 打卡按钮 -->
          <div class="flex justify-center my-8">
            <button id="checkin-btn" class="checkin-button bg-primary text-white w-24 h-24 rounded-full flex items-center justify-center text-2xl hover:bg-blue-600">
              <i class="fa fa-check"></i>
            </button>
          </div>

          <!-- 今日鼓励语 -->
          <div class="text-center mb-6">
            <p id="motivational-quote" class="text-gray-600 italic"></p>
          </div>
        </div>
      </section>

      <!-- 数据统计区域 -->
      <section id="stats-section" class="mb-8 hidden">
        <!-- 统计概览卡片 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <!-- 连续打卡 -->
          <div class="bg-white rounded-xl p-4 card-shadow border-l-4 border-blue-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">连续打卡</p>
                <h3 id="streak-count" class="text-2xl font-bold text-dark"></h3>
              </div>
              <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <i class="fa fa-calendar-check-o text-blue-500"></i>
              </div>
            </div>
            <div class="mt-2 text-xs text-green-500 flex items-center">
              <i class="fa fa-arrow-up mr-1"></i>
              <span id="streak-change">较上周</span>
            </div>
          </div>

          <!-- 总打卡天数 -->
          <div class="bg-white rounded-xl p-4 card-shadow border-l-4 border-green-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">总打卡天数</p>
                <h3 id="total-count" class="text-2xl font-bold text-dark"></h3>
              </div>
              <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <i class="fa fa-check-square-o text-green-500"></i>
              </div>
            </div>
            <div class="mt-2 text-xs text-green-500">
              <span id="total-progress">距离目标还有</span>
            </div>
          </div>

          <!-- 本月完成率 -->
          <div class="bg-white rounded-xl p-4 card-shadow border-l-4 border-purple-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">本月完成率</p>
                <h3 id="completion-rate" class="text-2xl font-bold text-dark"></h3>
              </div>
              <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                <i class="fa fa-pie-chart text-purple-500"></i>
              </div>
            </div>
            <div class="mt-2">
              <div class="w-full bg-gray-200 rounded-full h-1.5">
                <div id="rate-bar" class="bg-purple-500 h-1.5 rounded-full"></div>
              </div>
            </div>
          </div>

          <!-- 最长连续 -->
          <div class="bg-white rounded-xl p-4 card-shadow border-l-4 border-amber-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">最长连续</p>
                <h3 id="longest-streak" class="text-2xl font-bold text-dark"></h3>
              </div>
              <div class="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center">
                <i class="fa fa-trophy text-amber-500"></i>
              </div>
            </div>
            <div class="mt-2 text-xs text-gray-500" id="longest-streak-date"></div>
          </div>
        </div>

        <!-- 图表区域 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <!-- 周打卡情况 -->
          <div class="bg-white rounded-xl p-6 card-shadow">
            <h3 class="text-lg font-semibold text-dark mb-4">本周打卡情况</h3>
            <div class="h-64">
              <canvas id="weekly-chart"></canvas>
            </div>
          </div>

          <!-- 月度趋势 -->
          <div class="bg-white rounded-xl p-6 card-shadow">
            <h3 class="text-lg font-semibold text-dark mb-4">月度打卡趋势</h3>
            <div class="h-64">
              <canvas id="monthly-chart"></canvas>
            </div>
          </div>
        </div>

        <!-- 详细统计 -->
        <div class="bg-white rounded-xl p-6 card-shadow">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-dark">打卡详情</h3>
            <div class="flex gap-2">
              <button id="export-stats" class="text-sm px-3 py-1 bg-primary text-white rounded-lg hover:bg-blue-600 flex items-center gap-1">
                <i class="fa fa-download"></i>
                <span>导出数据</span>
              </button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日期</th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">连续天数</th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">备注</th>
                </tr>
              </thead>
              <tbody id="stats-table-body" class="bg-white divide-y divide-gray-200">
                <!-- 统计数据将通过 JavaScript 动态生成 -->
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 日历视图 -->
      <section id="calendar-section" class="mb-8 hidden">
        <div class="bg-white rounded-xl p-6 card-shadow">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl font-semibold text-dark">打卡日历</h3>
            <div class="flex items-center gap-3">
              <button id="prev-month" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-600">
                <i class="fa fa-chevron-left"></i>
              </button>
              <select id="month-selector" class="px-3 py-1 border border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary">
                <!-- 月份选项将通过 JavaScript 动态生成 -->
              </select>
              <button id="next-month" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-600">
                <i class="fa fa-chevron-right"></i>
              </button>
            </div>
          </div>
          
          <!-- 日历图例 -->
          <div class="flex flex-wrap mb-4 text-sm text-gray-600">
            <div class="calendar-legend-item">
              <div class="calendar-legend-color bg-primary"></div>
              <span>已完成</span>
            </div>
            <div class="calendar-legend-item">
              <div class="calendar-legend-color border-2 border-primary bg-white"></div>
              <span>今天</span>
            </div>
            <div class="calendar-legend-item">
              <div class="calendar-legend-color bg-gray-100"></div>
              <span>未完成</span>
            </div>
          </div>
          
          <!-- 星期标题 -->
          <div class="grid grid-cols-7 gap-2 mb-2">
            <div class="text-center text-sm font-medium text-gray-500 py-2">日</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">一</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">二</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">三</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">四</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">五</div>
            <div class="text-center text-sm font-medium text-gray-500 py-2">六</div>
          </div>
          
          <!-- 日历天数 -->
          <div id="calendar-days" class="grid grid-cols-7 gap-2">
            <!-- 日历天数将通过 JavaScript 动态生成 -->
          </div>
          
          <!-- 日历统计 -->
          <div class="mt-6 grid grid-cols-3 gap-4 text-center">
            <div class="bg-blue-50 rounded-lg p-3">
              <div class="text-sm text-gray-500">本月完成</div>
              <div id="month-completed" class="text-xl font-bold text-primary">0</div>
            </div>
            <div class="bg-green-50 rounded-lg p-3">
              <div class="text-sm text-gray-500">本月目标</div>
              <div id="month-target" class="text-xl font-bold text-green-500">0</div>
            </div>
            <div class="bg-purple-50 rounded-lg p-3">
              <div class="text-sm text-gray-500">完成率</div>
              <div id="month-rate" class="text-xl font-bold text-purple-500">0%</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 成就系统 -->
      <section id="achievements-section" class="mb-8 hidden">
        <div class="bg-white rounded-xl p-6 card-shadow">
          <h3 class="text-xl font-semibold text-dark mb-6">成就徽章</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6" id="achievements-container">
            <!-- 成就徽章将通过 JavaScript 动态生成 -->
          </div>
        </div>
      </section>
    </main>

    <!-- 底部导航 -->
    <footer class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-3 px-4">
      <div class="flex justify-around max-w-4xl mx-auto">
        <button class="nav-btn flex flex-col items-center text-primary" data-target="habit-details">
          <i class="fa fa-home text-xl"></i>
          <span class="text-xs mt-1">主页</span>
        </button>
        <button class="nav-btn flex flex-col items-center text-gray-500" data-target="stats-section">
          <i class="fa fa-bar-chart text-xl"></i>
          <span class="text-xs mt-1">统计</span>
        </button>
        <button class="nav-btn flex flex-col items-center text-gray-500" data-target="calendar-section">
          <i class="fa fa-calendar text-xl"></i>
          <span class="text-xs mt-1">日历</span>
        </button>
        <button class="nav-btn flex flex-col items-center text-gray-500" data-target="achievements-section">
          <i class="fa fa-trophy text-xl"></i>
          <span class="text-xs mt-1">成就</span>
        </button>
      </div>
    </footer>
  </div>

  <!-- 添加/编辑习惯模态框 -->
  <div id="habit-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
    <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
      <h3 id="modal-title" class="text-xl font-bold text-dark mb-6">添加新目标</h3>
      <form id="habit-form">
        <input type="hidden" id="habit-id">
        <div class="mb-4">
          <label for="habit-name-input" class="block text-gray-700 mb-2">习惯名称</label>
          <input type="text" id="habit-name-input" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary" placeholder="例如：每日阅读" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">选择图标</label>
          <div class="grid grid-cols-6 gap-3" id="icon-selector">
            <div class="icon-option w-12 h-12 rounded-full bg-red-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="book" data-color="#ef4444">
              <i class="fa fa-book"></i>
            </div>
            <div class="icon-option w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="running" data-color="#3b82f6">
              <i class="fa fa-running"></i>
            </div>
            <div class="icon-option w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="dumbbell" data-color="#10b981">
              <i class="fa fa-dumbbell"></i>
            </div>
            <div class="icon-option w-12 h-12 rounded-full bg-yellow-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="meditation" data-color="#f59e0b">
              <i class="fa fa-om"></i>
            </div>
            <div class="icon-option w-12 h-12 rounded-full bg-purple-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="water" data-color="#8b5cf6">
              <i class="fa fa-tint"></i>
            </div>
            <div class="icon-option w-12 h-12 rounded-full bg-pink-500 flex items-center justify-center text-white text-xl cursor-pointer" data-icon="music" data-color="#ec4899">
              <i class="fa fa-music"></i>
            </div>
          </div>
        </div>
        <div class="mb-6">
          <label for="reminder-time" class="block text-gray-700 mb-2">提醒时间（可选）</label>
          <input type="time" id="reminder-time" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
        </div>
        <div class="flex gap-3">
          <button type="button" id="cancel-modal" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100">取消</button>
          <button type="submit" class="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600">保存</button>
        </div>
      </form>
    </div>
  </div>

  <!-- 成就解锁提示 -->
  <div id="achievement-toast" class="fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 flex items-center gap-3 transform translate-x-full transition-transform duration-300 z-50">
    <div class="w-10 h-10 rounded-full bg-yellow-100 flex items-center justify-center">
      <i class="fa fa-trophy text-yellow-500"></i>
    </div>
    <div>
      <h4 class="font-semibold text-dark">成就解锁！</h4>
      <p id="achievement-message" class="text-sm text-gray-600"></p>
    </div>
  </div>

  <script>
    // 全局变量
    let habits = [];
    let currentHabitId = null;
    let currentDate = new Date();
    let selectedIcon = 'book';
    let selectedColor = '#ef4444';

    // 鼓励语句数组
    const motivationalQuotes = [
      "太棒了！你正在一步步接近目标！",
      "坚持就是胜利，今天你又进步了一点！",
      "每一次打卡都是对自己的承诺，你做到了！",
      "习惯的力量是巨大的，继续保持！",
      "你已经比昨天的自己更好了！",
      "小步前进也是前进，为你点赞！",
      "每一天的坚持都会在未来绽放！",
      "你正在建立一个更好的自己！",
      "今天的努力，明天的收获！",
      "继续保持这种势头，你真棒！"
    ];

    // 成就定义
    const achievements = [
      { id: 'streak-7', name: '一周坚持', description: '连续打卡7天', icon: '7days', requirement: { type: 'streak', value: 7 } },
      { id: 'streak-30', name: '月度达人', description: '连续打卡30天', icon: '30days', requirement: { type: 'streak', value: 30 } },
      { id: 'streak-100', name: '百日不断', description: '连续打卡100天', icon: '100days', requirement: { type: 'streak', value: 100 } },
      { id: 'total-50', name: '半百成就', description: '累计打卡50天', icon: '50days', requirement: { type: 'total', value: 50 } },
      { id: 'total-200', name: '打卡达人', description: '累计打卡200天', icon: '200days', requirement: { type: 'total', value: 200 } },
      { id: 'total-365', name: '年度传奇', description: '累计打卡365天', icon: '365days', requirement: { type: 'total', value: 365 } }
    ];

    // 成就图标URL
    const achievementIcons = {
      '7days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D',
      '30days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D',
      '100days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D',
      '50days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D',
      '200days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D',
      '365days': 'https://p3-flow-imagex-sign.byteimg.com/tos-cn-i-a9rns2rl98/rc/pc/super_tool/f2bd7c6302ed461a845427e1315ba515~tplv-a9rns2rl98-image.image?rcl=20251205005141DFC957D08C42D5EAEFAF&rk3s=8e244e95&rrcfp=f06b921b&x-expires=1767459113&x-signature=5grVeu9X3t8XW4lMgyRl7WpcMx0%3D'
    };

    // 习惯图标映射
    const habitIcons = {
      'book': 'fa-book',
      'running': 'fa-running',
      'dumbbell': 'fa-dumbbell',
      'meditation': 'fa-om',
      'water': 'fa-tint',
      'music': 'fa-music'
    };

    // DOM 元素
    const habitsContainer = document.getElementById('habits-container');
    const habitDetails = document.getElementById('habit-details');
    const statsSection = document.getElementById('stats-section');
    const calendarSection = document.getElementById('calendar-section');
    const achievementsSection = document.getElementById('achievements-section');
    const checkinBtn = document.getElementById('checkin-btn');
    const addHabitBtn = document.getElementById('add-habit-btn');
    const editHabitBtn = document.getElementById('edit-habit-btn');
    const habitModal = document.getElementById('habit-modal');
    const modalTitle = document.getElementById('modal-title');
    const habitForm = document.getElementById('habit-form');
    const cancelModalBtn = document.getElementById('cancel-modal');
    const habitNameInput = document.getElementById('habit-name-input');
    const habitIdInput = document.getElementById('habit-id');
    const reminderTimeInput = document.getElementById('reminder-time');
    const iconSelector = document.getElementById('icon-selector');
    const iconOptions = document.querySelectorAll('.icon-option');
    const navBtns = document.querySelectorAll('.nav-btn');
    const achievementToast = document.getElementById('achievement-toast');
    const achievementMessage = document.getElementById('achievement-message');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const currentMonthSpan = document.getElementById('current-month');
    const calendarDays = document.getElementById('calendar-days');
    const motivationalQuoteEl = document.getElementById('motivational-quote');

    // 初始化应用
    function initApp() {
      loadHabits();
      setupEventListeners();
      renderHabits();
      setupReminders();
      
      // 如果有习惯，选择第一个
      if (habits.length > 0) {
        selectHabit(habits[0].id);
      }
    }

    // 从本地存储加载习惯
    function loadHabits() {
      const storedHabits = localStorage.getItem('dailyCheckinHabits');
      if (storedHabits) {
        habits = JSON.parse(storedHabits);
      }
    }

    // 保存习惯到本地存储
    function saveHabits() {
      localStorage.setItem('dailyCheckinHabits', JSON.stringify(habits));
    }

    // 设置事件监听器
    function setupEventListeners() {
      // 添加目标打卡按钮
      addHabitBtn.addEventListener('click', () => {
        openHabitModal();
      });

      // 编辑习惯按钮
      editHabitBtn.addEventListener('click', () => {
        if (currentHabitId) {
          const habit = habits.find(h => h.id === currentHabitId);
          if (habit) {
            openHabitModal(habit);
          }
        }
      });

      // 打卡按钮
      checkinBtn.addEventListener('click', () => {
        if (currentHabitId) {
          toggleCheckin(currentHabitId);
        }
      });

      // 习惯表单提交
      habitForm.addEventListener('submit', (e) => {
        e.preventDefault();
        saveHabit();
      });

      // 取消模态框
      cancelModalBtn.addEventListener('click', () => {
        closeHabitModal();
      });

      // 图标选择
      iconOptions.forEach(option => {
        option.addEventListener('click', () => {
          iconOptions.forEach(opt => opt.classList.remove('ring-2', 'ring-primary'));
          option.classList.add('ring-2', 'ring-primary');
          selectedIcon = option.dataset.icon;
          selectedColor = option.dataset.color;
        });
      });

      // 导航按钮
      navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          const target = btn.dataset.target;
          showSection(target);
          
          // 更新导航按钮样式
          navBtns.forEach(b => {
            b.classList.remove('text-primary');
            b.classList.add('text-gray-500');
          });
          btn.classList.remove('text-gray-500');
          btn.classList.add('text-primary');
        });
      });

      // 日历导航
      prevMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
      });

      nextMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
      });

      // 点击模态框外部关闭
      habitModal.addEventListener('click', (e) => {
        if (e.target === habitModal) {
          closeHabitModal();
        }
      });
    }

    // 渲染习惯卡片
    function renderHabits() {
      habitsContainer.innerHTML = '';
      
      if (habits.length === 0) {
        habitsContainer.innerHTML = `
          <div class="flex flex-col items-center justify-center w-full py-12 text-gray-500">
            <i class="fa fa-calendar-check-o text-4xl mb-4"></i>
            <p>还没有添加任何习惯</p>
            <p class="text-sm">点击右上角"添加目标打卡"开始</p>
          </div>
        `;
        return;
      }
      
      habits.forEach(habit => {
        const card = document.createElement('div');
        card.className = `habit-card flex-shrink-0 w-32 bg-white rounded-xl p-4 flex flex-col items-center cursor-pointer card-shadow ${currentHabitId === habit.id ? 'active' : ''}`;
        
        const isCompletedToday = isHabitCompletedToday(habit.id);
        
        card.innerHTML = `
          <div class="w-12 h-12 rounded-full flex items-center justify-center text-white text-xl mb-3" style="background-color: ${habit.color}">
            <i class="fa ${habitIcons[habit.icon] || 'fa-calendar-check-o'}"></i>
          </div>
          <h3 class="text-center font-medium text-dark mb-1">${habit.name}</h3>
          <div class="w-full bg-gray-200 rounded-full h-1.5">
            <div class="bg-primary h-1.5 rounded-full" style="width: ${getMonthlyCompletionRate(habit.id)}%"></div>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            ${getStreakCount(habit.id)}天
          </div>
          ${isCompletedToday ? '<div class="absolute top-2 right-2 w-4 h-4 bg-green-500 rounded-full"></div>' : ''}
        `;
        
        card.addEventListener('click', () => {
          selectHabit(habit.id);
        });
        
        habitsContainer.appendChild(card);
      });
    }

    // 选择习惯
    function selectHabit(habitId) {
      currentHabitId = habitId;
      renderHabits();
      renderHabitDetails();
      renderStats();
      renderCalendar();
      renderAchievements();
      showSection('habit-details');
      
      // 更新导航按钮样式
      navBtns.forEach(btn => {
        if (btn.dataset.target === 'habit-details') {
          btn.classList.remove('text-gray-500');
          btn.classList.add('text-primary');
        } else {
          btn.classList.remove('text-primary');
          btn.classList.add('text-gray-500');
        }
      });
    }

    // 渲染习惯详情
    function renderHabitDetails() {
      if (!currentHabitId) return;
      
      const habit = habits.find(h => h.id === currentHabitId);
      if (!habit) return;
      
      const habitIcon = document.getElementById('habit-icon');
      const habitName = document.getElementById('habit-name');
      const habitStreak = document.getElementById('habit-streak');
      
      habitIcon.style.backgroundColor = habit.color;
      habitIcon.innerHTML = `<i class="fa ${habitIcons[habit.icon] || 'fa-calendar-check-o'}"></i>`;
      habitName.textContent = habit.name;
      
      const streak = getStreakCount(habit.id);
      habitStreak.textContent = streak > 0 ? `已连续打卡 ${streak} 天` : '开始你的打卡之旅吧！';
      
      // 更新打卡按钮状态
      const isCompletedToday = isHabitCompletedToday(habit.id);
      if (isCompletedToday) {
        checkinBtn.classList.add('completed');
        checkinBtn.innerHTML = '<i class="fa fa-check"></i>';
      } else {
        checkinBtn.classList.remove('completed');
        checkinBtn.innerHTML = '<i class="fa fa-check"></i>';
      }
      
      // 显示随机鼓励语
      motivationalQuoteEl.textContent = getRandomQuote();
      
      habitDetails.classList.remove('hidden');
      statsSection.classList.add('hidden');
      calendarSection.classList.add('hidden');
      achievementsSection.classList.add('hidden');
    }

    // 渲染统计数据
    function renderStats() {
      if (!currentHabitId) return;
      
      const habit = habits.find(h => h.id === currentHabitId);
      if (!habit) return;
      
      // 更新基础统计数据
      const streakCount = document.getElementById('streak-count');
      const totalCount = document.getElementById('total-count');
      const completionRate = document.getElementById('completion-rate');
      const longestStreak = document.getElementById('longest-streak');
      const streakChange = document.getElementById('streak-change');
      const totalProgress = document.getElementById('total-progress');
      const longestStreakDate = document.getElementById('longest-streak-date');
      const rateBar = document.getElementById('rate-bar');
      
      const currentStreak = getStreakCount(habit.id);
      const totalDays = getTotalCount(habit.id);
      const monthlyRate = getMonthlyCompletionRate(habit.id);
      const maxStreak = getLongestStreak(habit.id);
      
      // 更新显示
      streakCount.textContent = `${currentStreak}天`;
      totalCount.textContent = `${totalDays}天`;
      completionRate.textContent = `${monthlyRate}%`;
      longestStreak.textContent = `${maxStreak}天`;
      
      // 更新进度条
      rateBar.style.width = `${monthlyRate}%`;
      
      // 计算并显示额外信息
      const lastWeekStreak = getStreakCountLastWeek(habit.id);
      const streakDiff = currentStreak - lastWeekStreak;
      streakChange.textContent = streakDiff >= 0 ? `较上周+${streakDiff}天` : `较上周${streakDiff}天`;
      streakChange.parentElement.className = streakDiff >= 0 ? 'mt-2 text-xs text-green-500 flex items-center' : 'mt-2 text-xs text-red-500 flex items-center';
      
      // 目标进度（假设目标是365天）
      const targetDays = 365;
      const daysLeft = Math.max(0, targetDays - totalDays);
      totalProgress.textContent = daysLeft > 0 ? `距离目标还有${daysLeft}天` : '已达成目标！';
      
      // 最长连续日期范围
      const longestStreakRange = getLongestStreakRange(habit.id);
      if (longestStreakRange) {
        longestStreakDate.textContent = `${formatDateForDisplay(longestStreakRange.start)} - ${formatDateForDisplay(longestStreakRange.end)}`;
      } else {
        longestStreakDate.textContent = '暂无记录';
      }
      
      // 渲染图表
      renderWeeklyChart(habit);
      renderMonthlyChart(habit);
      
      // 渲染详细统计表格
      renderStatsTable(habit);
      
      // 设置导出按钮事件
      document.getElementById('export-stats').onclick = () => exportStats(habit);
    }
    
    // 获取上周的连续打卡天数
    function getStreakCountLastWeek(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins || habit.checkins.length === 0) return 0;
      
      // 计算上周的日期
      const lastWeek = new Date();
      lastWeek.setDate(lastWeek.getDate() - 7);
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      // 从上周开始往前检查
      let streak = 0;
      const checkDate = new Date(lastWeek);
      
      for (let i = 0; i < 365; i++) { // 最多检查一年
        checkDate.setDate(lastWeek.getDate() - i);
        const dateString = formatDate(checkDate);
        
        if (sortedCheckins.includes(dateString)) {
          streak++;
        } else {
          break;
        }
      }
      
      return streak;
    }
    
    // 获取最长连续打卡的日期范围
    function getLongestStreakRange(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins || habit.checkins.length === 0) return null;
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      let maxStreak = 1;
      let currentStreak = 1;
      let maxStart = sortedCheckins[0];
      let maxEnd = sortedCheckins[0];
      let currentStart = sortedCheckins[0];
      
      for (let i = 1; i < sortedCheckins.length; i++) {
        const prevDate = new Date(sortedCheckins[i - 1]);
        const currDate = new Date(sortedCheckins[i]);
        
        // 计算日期差
        const diffTime = currDate - prevDate;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
          // 连续天数
          currentStreak++;
          if (currentStreak > maxStreak) {
            maxStreak = currentStreak;
            maxStart = currentStart;
            maxEnd = sortedCheckins[i];
          }
        } else {
          // 中断了，重置计数
          currentStreak = 1;
          currentStart = sortedCheckins[i];
        }
      }
      
      return {
        start: new Date(maxStart),
        end: new Date(maxEnd),
        length: maxStreak
      };
    }
    
    // 格式化日期显示
    function formatDateForDisplay(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
    
    // 渲染周打卡图表
    function renderWeeklyChart(habit) {
      const ctx = document.getElementById('weekly-chart').getContext('2d');
      
      // 销毁旧图表
      if (window.weeklyChart) {
        window.weeklyChart.destroy();
      }
      
      // 准备数据
      const today = new Date();
      const labels = [];
      const data = [];
      
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        
        // 格式化日期为星期几
        const dayNames = ['日', '一', '二', '三', '四', '五', '六'];
        labels.push(`周${dayNames[date.getDay()]}`);
        
        // 检查是否打卡
        const dateString = formatDate(date);
        data.push(habit.checkins && habit.checkins.includes(dateString) ? 1 : 0);
      }
      
      // 创建图表
      window.weeklyChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: '打卡状态',
            data: data,
            backgroundColor: data.map(d => d === 1 ? '#3b82f6' : '#e5e7eb'),
            borderColor: data.map(d => d === 1 ? '#2563eb' : '#d1d5db'),
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 1,
              ticks: {
                stepSize: 1,
                callback: function(value) {
                  return value === 1 ? '已打卡' : '未打卡';
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return context.parsed.y === 1 ? '已打卡' : '未打卡';
                }
              }
            }
          }
        }
      });
    }
    
    // 渲染月度趋势图表
    function renderMonthlyChart(habit) {
      const ctx = document.getElementById('monthly-chart').getContext('2d');
      
      // 销毁旧图表
      if (window.monthlyChart) {
        window.monthlyChart.destroy();
      }
      
      // 准备数据 - 最近6个月
      const today = new Date();
      const labels = [];
      const data = [];
      
      for (let i = 5; i >= 0; i--) {
        const date = new Date(today);
        date.setMonth(today.getMonth() - i);
        
        // 格式化日期为月份
        labels.push(`${date.getFullYear()}年${date.getMonth() + 1}月`);
        
        // 计算当月完成天数
        const year = date.getFullYear();
        const month = date.getMonth();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        let completedDays = 0;
        if (habit.checkins) {
          completedDays = habit.checkins.filter(dateString => {
            const checkDate = new Date(dateString);
            return checkDate.getFullYear() === year && checkDate.getMonth() === month;
          }).length;
        }
        
        // 计算完成率
        const daysPassed = (year === today.getFullYear() && month === today.getMonth()) 
          ? today.getDate() 
          : daysInMonth;
        
        const rate = daysPassed > 0 ? Math.round((completedDays / daysPassed) * 100) : 0;
        data.push(rate);
      }
      
      // 创建图表
      window.monthlyChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '月度完成率',
            data: data,
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderColor: '#3b82f6',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointBackgroundColor: '#3b82f6',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `完成率: ${context.parsed.y}%`;
                }
              }
            }
          }
        }
      });
    }
    
    // 渲染详细统计表格
    function renderStatsTable(habit) {
      const tableBody = document.getElementById('stats-table-body');
      tableBody.innerHTML = '';
      
      if (!habit.checkins || habit.checkins.length === 0) {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `
          <td colspan="4" class="px-6 py-8 text-center text-gray-500">
            暂无打卡记录
          </td>
        `;
        tableBody.appendChild(emptyRow);
        return;
      }
      
      // 按日期排序（最近的在前）
      const sortedCheckins = [...habit.checkins].sort().reverse();
      
      // 最多显示最近30条记录
      const recentCheckins = sortedCheckins.slice(0, 30);
      
      recentCheckins.forEach((dateString, index) => {
        const date = new Date(dateString);
        const row = document.createElement('tr');
        
        // 计算当天的连续天数
        const streakAtDate = calculateStreakAtDate(habit, date);
        
        row.innerHTML = `
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">${formatDateForDisplay(date)}</div>
            <div class="text-xs text-gray-500">${getDayOfWeek(date)}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
              已完成
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            ${streakAtDate}天
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            ${getMotivationalNote(streakAtDate)}
          </td>
        `;
        
        tableBody.appendChild(row);
      });
    }
    
    // 计算指定日期的连续打卡天数
    function calculateStreakAtDate(habit, targetDate) {
      if (!habit.checkins) return 0;
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      let streak = 0;
      const checkDate = new Date(targetDate);
      
      for (let i = 0; i < 365; i++) { // 最多检查一年
        const dateString = formatDate(checkDate);
        
        if (sortedCheckins.includes(dateString)) {
          streak++;
          checkDate.setDate(checkDate.getDate() - 1);
        } else {
          break;
        }
      }
      
      return streak;
    }
    
    // 获取星期几
    function getDayOfWeek(date) {
      const dayNames = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
      return dayNames[date.getDay()];
    }
    
    // 获取鼓励备注
    function getMotivationalNote(streak) {
      if (streak >= 30) {
        return '太棒了！你已连续打卡30天以上！';
      } else if (streak >= 21) {
        return '习惯已初步养成，继续保持！';
      } else if (streak >= 14) {
        return '两周了！你正在变得更好！';
      } else if (streak >= 7) {
        return '一周了！坚持的力量！';
      } else {
        return '加油！每一天都很重要！';
      }
    }
    
    // 导出统计数据
    function exportStats(habit) {
      if (!habit.checkins || habit.checkins.length === 0) {
        alert('暂无数据可导出');
        return;
      }
      
      // 准备CSV数据
      let csvContent = "日期,状态,连续天数,备注\n";
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      sortedCheckins.forEach(dateString => {
        const date = new Date(dateString);
        const streak = calculateStreakAtDate(habit, date);
        const note = getMotivationalNote(streak);
        
        csvContent += `${formatDateForDisplay(date)},已完成,${streak}天,"${note}"\n`;
      });
      
      // 创建下载链接
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `${habit.name}_打卡记录.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // 渲染日历
    function renderCalendar() {
      if (!currentHabitId) return;
      
      const habit = habits.find(h => h.id === currentHabitId);
      if (!habit) return;
      
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth();
      
      // 更新月份选择器
      updateMonthSelector(year, month);
      
      // 获取当月第一天是星期几
      const firstDay = new Date(year, month, 1).getDay();
      
      // 获取当月的天数
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      
      // 获取上个月的天数
      const prevMonthDays = new Date(year, month, 0).getDate();
      
      // 清空日历
      calendarDays.innerHTML = '';
      
      // 添加上个月的日期
      for (let i = firstDay - 1; i >= 0; i--) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day flex items-center justify-center calendar-day-other-month';
        dayElement.textContent = prevMonthDays - i;
        calendarDays.appendChild(dayElement);
      }
      
      // 添加当月日期
      const today = new Date();
      const isCurrentMonth = today.getFullYear() === year && today.getMonth() === month;
      let completedDays = 0;
      
      for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day flex items-center justify-center';
        
        const date = new Date(year, month, day);
        const dateString = formatDate(date);
        
        // 检查是否完成
        const isCompleted = habit.checkins && habit.checkins.includes(dateString);
        
        if (isCompleted) {
          dayElement.classList.add('calendar-day-completed');
          completedDays++;
        }
        
        // 检查是否是今天
        if (isCurrentMonth && today.getDate() === day) {
          dayElement.classList.add('calendar-day-today');
        }
        
        // 添加日期数字
        dayElement.textContent = day;
        
        // 添加点击事件，显示提示
        dayElement.addEventListener('click', () => {
          showDayTooltip(date, isCompleted);
        });
        
        calendarDays.appendChild(dayElement);
      }
      
      // 计算并显示月度统计
      updateMonthStats(year, month, completedDays, daysInMonth);
    }
    
    // 更新月份选择器
    function updateMonthSelector(year, month) {
      const monthSelector = document.getElementById('month-selector');
      monthSelector.innerHTML = '';
      
      // 生成未来12个月的选项
      for (let i = 0; i < 12; i++) {
        const optionDate = new Date(year, month + i, 1);
        const optionYear = optionDate.getFullYear();
        const optionMonth = optionDate.getMonth();
        const optionText = `${optionYear}年${optionMonth + 1}月`;
        
        const option = document.createElement('option');
        option.value = `${optionYear}-${optionMonth}`;
        option.textContent = optionText;
        
        if (optionYear === year && optionMonth === month) {
          option.selected = true;
        }
        
        monthSelector.appendChild(option);
      }
      
      // 添加事件监听
      monthSelector.onchange = (e) => {
        const [selectedYear, selectedMonth] = e.target.value.split('-').map(Number);
        currentDate = new Date(selectedYear, selectedMonth, 1);
        renderCalendar();
      };
    }
    
    // 显示日期提示
    function showDayTooltip(date, isCompleted) {
      // 创建提示元素
      let tooltip = document.getElementById('day-tooltip');
      if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.id = 'day-tooltip';
        tooltip.className = 'fixed bg-dark text-white p-2 rounded text-sm z-50 shadow-lg';
        document.body.appendChild(tooltip);
      }
      
      // 设置提示内容
      const dateStr = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
      const status = isCompleted ? '已完成' : '未完成';
      tooltip.innerHTML = `
        <div>${dateStr}</div>
        <div>状态：<span class="${isCompleted ? 'text-green-400' : 'text-red-400'}">${status}</span></div>
      `;
      
      // 显示提示
      tooltip.style.display = 'block';
      
      // 定位提示
      document.addEventListener('mousemove', updateTooltipPosition);
      
      // 3秒后隐藏提示
      setTimeout(() => {
        tooltip.style.display = 'none';
        document.removeEventListener('mousemove', updateTooltipPosition);
      }, 3000);
    }
    
    // 更新提示位置
    function updateTooltipPosition(e) {
      const tooltip = document.getElementById('day-tooltip');
      if (tooltip) {
        tooltip.style.left = `${e.clientX + 10}px`;
        tooltip.style.top = `${e.clientY - 30}px`;
      }
    }
    
    // 更新月度统计
    function updateMonthStats(year, month, completedDays, totalDays) {
      const monthCompleted = document.getElementById('month-completed');
      const monthTarget = document.getElementById('month-target');
      const monthRate = document.getElementById('month-rate');
      
      // 获取当月已过的天数
      const today = new Date();
      let daysPassed = totalDays;
      
      if (today.getFullYear() === year && today.getMonth() === month) {
        daysPassed = today.getDate();
      }
      
      // 计算目标天数（默认为当月天数）
      const targetDays = totalDays;
      
      // 计算完成率
      const rate = daysPassed > 0 ? Math.round((completedDays / daysPassed) * 100) : 0;
      
      // 更新显示
      monthCompleted.textContent = completedDays;
      monthTarget.textContent = targetDays;
      monthRate.textContent = `${rate}%`;
    }

    // 渲染成就
    function renderAchievements() {
      if (!currentHabitId) return;
      
      const habit = habits.find(h => h.id === currentHabitId);
      if (!habit) return;
      
      const achievementsContainer = document.getElementById('achievements-container');
      achievementsContainer.innerHTML = '';
      
      // 计算成就统计
      const unlockedCount = achievements.filter(a => checkAchievement(habit, a)).length;
      const totalCount = achievements.length;
      const completionRate = Math.round((unlockedCount / totalCount) * 100);
      
      // 添加成就统计信息
      const statsDiv = document.createElement('div');
      statsDiv.className = 'mb-6 text-center';
      statsDiv.innerHTML = `
        <div class="inline-flex items-center bg-primary/10 rounded-full px-4 py-2">
          <div class="w-3 h-3 bg-primary rounded-full mr-2 animate-pulse"></div>
          <span class="text-sm font-medium text-primary">已解锁 ${unlockedCount}/${totalCount} 个成就</span>
          <span class="ml-2 text-xs text-gray-500">(${completionRate}%)</span>
        </div>
      `;
      achievementsContainer.appendChild(statsDiv);
      
      // 按类别分组显示成就
      const groupedAchievements = {
        '连续打卡': achievements.filter(a => a.requirement.type === 'streak'),
        '累计打卡': achievements.filter(a => a.requirement.type === 'total')
      };
      
      Object.entries(groupedAchievements).forEach(([category, items]) => {
        // 添加类别标题
        const categoryTitle = document.createElement('h3');
        categoryTitle.className = 'text-lg font-bold text-dark mb-4';
        categoryTitle.textContent = category;
        achievementsContainer.appendChild(categoryTitle);
        
        // 添加类别成就
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6';
        
        items.forEach(achievement => {
          const isUnlocked = checkAchievement(habit, achievement);
          const progress = getAchievementProgress(habit, achievement);
          
          const badge = document.createElement('div');
          badge.className = `achievement-badge flex flex-col items-center p-4 bg-white rounded-xl card-shadow transition-all duration-300 ${
            isUnlocked ? 'ring-2 ring-primary ring-offset-2' : 'opacity-70 hover:opacity-100'
          }`;
          
          // 生成进度条
          const progressBar = progress < 100 ? `
            <div class="w-full bg-gray-200 rounded-full h-1.5 mt-2">
              <div class="bg-accent h-1.5 rounded-full transition-all duration-500" style="width: ${progress}%"></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">${progress}%</div>
          ` : '';
          
          badge.innerHTML = `
            <div class="w-16 h-16 mb-3 relative">
              <div class="absolute inset-0 bg-primary/10 rounded-full animate-ping opacity-75 ${isUnlocked ? '' : 'hidden'}"></div>
              <img src="${achievementIcons[achievement.icon]}" alt="${achievement.name}" 
                   class="w-full h-full object-contain relative z-10 transition-transform duration-300 ${
                     isUnlocked ? 'scale-110' : ''
                   }">
              ${isUnlocked ? '<div class="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center text-white text-xs">✓</div>' : ''}
            </div>
            <h4 class="font-medium text-dark text-center">${achievement.name}</h4>
            <p class="text-xs text-gray-500 text-center mb-2">${achievement.description}</p>
            ${progressBar}
          `;
          
          categoryDiv.appendChild(badge);
        });
        
        achievementsContainer.appendChild(categoryDiv);
      });
    }
    
    // 获取成就进度
    function getAchievementProgress(habit, achievement) {
      const { type, value } = achievement.requirement;
      let currentValue = 0;
      
      if (type === 'streak') {
        currentValue = getStreakCount(habit.id);
      } else if (type === 'total') {
        currentValue = getTotalCount(habit.id);
      }
      
      return Math.min(Math.round((currentValue / value) * 100), 100);
    }

    // 打开习惯模态框
    function openHabitModal(habit = null) {
      if (habit) {
        modalTitle.textContent = '编辑习惯';
        habitIdInput.value = habit.id;
        habitNameInput.value = habit.name;
        reminderTimeInput.value = habit.reminderTime || '';
        
        // 选择图标
        iconOptions.forEach(opt => {
          opt.classList.remove('ring-2', 'ring-primary');
          if (opt.dataset.icon === habit.icon) {
            opt.classList.add('ring-2', 'ring-primary');
            selectedIcon = habit.icon;
            selectedColor = habit.color;
          }
        });
      } else {
        modalTitle.textContent = '添加新目标';
        habitForm.reset();
        habitIdInput.value = '';
        
        // 默认选择第一个图标
        iconOptions.forEach((opt, index) => {
          if (index === 0) {
            opt.classList.add('ring-2', 'ring-primary');
            selectedIcon = opt.dataset.icon;
            selectedColor = opt.dataset.color;
          } else {
            opt.classList.remove('ring-2', 'ring-primary');
          }
        });
      }
      
      habitModal.classList.remove('hidden');
    }

    // 关闭习惯模态框
    function closeHabitModal() {
      habitModal.classList.add('hidden');
    }

    // 保存习惯
    function saveHabit() {
      const id = habitIdInput.value || generateId();
      const name = habitNameInput.value.trim();
      const reminderTime = reminderTimeInput.value;
      
      if (!name) {
        alert('请输入习惯名称');
        return;
      }
      
      const habitIndex = habits.findIndex(h => h.id === id);
      
      if (habitIndex >= 0) {
        // 更新现有习惯
        habits[habitIndex] = {
          ...habits[habitIndex],
          name,
          icon: selectedIcon,
          color: selectedColor,
          reminderTime
        };
      } else {
        // 添加新目标
        habits.push({
          id,
          name,
          icon: selectedIcon,
          color: selectedColor,
          reminderTime,
          checkins: [],
          achievements: []
        });
      }
      
      saveHabits();
      renderHabits();
      
      // 如果是新习惯，选择它
      if (habitIndex < 0) {
        selectHabit(id);
      } else if (currentHabitId === id) {
        // 如果编辑的是当前习惯，更新详情
        renderHabitDetails();
        renderStats();
        renderCalendar();
        renderAchievements();
      }
      
      closeHabitModal();
      setupReminders();
    }

    // 删除习惯
    function deleteHabit(habitId) {
      if (confirm('确定要删除这个习惯吗？所有打卡记录也将被删除。')) {
        habits = habits.filter(h => h.id !== habitId);
        saveHabits();
        renderHabits();
        
        // 如果删除的是当前习惯，选择第一个习惯
        if (currentHabitId === habitId) {
          if (habits.length > 0) {
            selectHabit(habits[0].id);
          } else {
            currentHabitId = null;
            habitDetails.classList.add('hidden');
            statsSection.classList.add('hidden');
            calendarSection.classList.add('hidden');
            achievementsSection.classList.add('hidden');
          }
        }
      }
    }

    // 切换打卡状态
    function toggleCheckin(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit) return;
      
      const today = formatDate(new Date());
      const checkinIndex = habit.checkins ? habit.checkins.indexOf(today) : -1;
      
      if (checkinIndex >= 0) {
        // 已经完成打卡，显示提示
        showAlreadyCheckedInMessage();
      } else {
        // 完成打卡
        if (!habit.checkins) {
          habit.checkins = [];
        }
        habit.checkins.push(today);
        checkinBtn.classList.add('completed', 'animate-pulse-short');
        setTimeout(() => {
          checkinBtn.classList.remove('animate-pulse-short');
        }, 500);
        
        // 显示鼓励语
        showMotivationalMessage();
        
        // 检查成就
        checkNewAchievements(habit);
        
        // 保存并更新UI
        saveHabits();
        renderHabits();
        renderHabitDetails();
        renderStats();
        renderCalendar();
        renderAchievements();
      }
    }
    
    // 显示已经打卡的提示
    function showAlreadyCheckedInMessage() {
      motivationalQuoteEl.textContent = "你今天已经完成打卡了，真棒！";
      motivationalQuoteEl.classList.add('animate-pulse');
      
      setTimeout(() => {
        motivationalQuoteEl.classList.remove('animate-pulse');
      }, 1000);
    }

    // 检查今天是否已打卡
    function isHabitCompletedToday(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins) return false;
      
      const today = formatDate(new Date());
      return habit.checkins.includes(today);
    }

    // 获取连续打卡天数
    function getStreakCount(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins || habit.checkins.length === 0) return 0;
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      // 从今天开始往前检查
      let streak = 0;
      const today = new Date();
      
      for (let i = 0; i < 365; i++) { // 最多检查一年
        const checkDate = new Date(today);
        checkDate.setDate(today.getDate() - i);
        const dateString = formatDate(checkDate);
        
        if (sortedCheckins.includes(dateString)) {
          streak++;
        } else {
          break;
        }
      }
      
      return streak;
    }

    // 获取总打卡天数
    function getTotalCount(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins) return 0;
      
      return habit.checkins.length;
    }

    // 获取月度完成率
    function getMonthlyCompletionRate(habitId, targetDate = new Date()) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins) return 0;
      
      const today = new Date();
      const currentYear = today.getFullYear();
      const currentMonth = today.getMonth();
      const currentDay = today.getDate();
      
      const targetYear = targetDate.getFullYear();
      const targetMonth = targetDate.getMonth();
      
      // 获取当月的天数
      const daysInMonth = new Date(targetYear, targetMonth + 1, 0).getDate();
      
      // 计算当月已过的天数（不包括今天之后的日期）
      let daysPassed;
      if (targetYear === currentYear && targetMonth === currentMonth) {
        // 当前月份：只计算到今天
        daysPassed = currentDay;
      } else if (targetYear < currentYear || (targetYear === currentYear && targetMonth < currentMonth)) {
        // 过去的月份：计算整个月
        daysPassed = daysInMonth;
      } else {
        // 未来的月份：返回0
        return 0;
      }
      
      // 计算当月完成的天数
      const completedDays = habit.checkins.filter(dateString => {
        const date = new Date(dateString);
        return date.getFullYear() === targetYear && date.getMonth() === targetMonth;
      }).length;
      
      // 计算完成率（确保不超过100%）
      const rate = daysPassed > 0 ? Math.round((completedDays / daysPassed) * 100) : 0;
      return Math.min(rate, 100);
    }

    // 获取最长连续打卡天数
    function getLongestStreak(habitId) {
      const habit = habits.find(h => h.id === habitId);
      if (!habit || !habit.checkins || habit.checkins.length === 0) return 0;
      
      // 按日期排序
      const sortedCheckins = [...habit.checkins].sort();
      
      let longestStreak = 1;
      let currentStreak = 1;
      
      for (let i = 1; i < sortedCheckins.length; i++) {
        const prevDate = new Date(sortedCheckins[i - 1]);
        const currDate = new Date(sortedCheckins[i]);
        
        // 计算日期差
        const diffTime = currDate - prevDate;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
          // 连续天数
          currentStreak++;
          longestStreak = Math.max(longestStreak, currentStreak);
        } else {
          // 中断了，重置计数
          currentStreak = 1;
        }
      }
      
      return longestStreak;
    }

    // 检查成就
    function checkAchievement(habit, achievement) {
      if (!habit.achievements) return false;
      
      // 如果已经解锁，直接返回
      if (habit.achievements.includes(achievement.id)) {
        return true;
      }
      
      const { type, value } = achievement.requirement;
      
      if (type === 'streak') {
        return getStreakCount(habit.id) >= value;
      } else if (type === 'total') {
        return getTotalCount(habit.id) >= value;
      }
      
      return false;
    }

    // 检查新成就
    function checkNewAchievements(habit) {
      if (!habit.achievements) {
        habit.achievements = [];
      }
      
      let newAchievements = [];
      
      achievements.forEach(achievement => {
        if (!habit.achievements.includes(achievement.id) && checkAchievement(habit, achievement)) {
          habit.achievements.push(achievement.id);
          newAchievements.push(achievement);
        }
      });
      
      // 显示新成就通知
      if (newAchievements.length > 0) {
        showAchievementToast(newAchievements[0]);
      }
    }

    // 显示成就解锁提示
    function showAchievementToast(achievement) {
      achievementMessage.textContent = `恭喜获得"${achievement.name}"成就！`;
      achievementToast.classList.remove('translate-x-full');
      
      setTimeout(() => {
        achievementToast.classList.add('translate-x-full');
      }, 3000);
    }

    // 显示鼓励消息
    function showMotivationalMessage() {
      motivationalQuoteEl.textContent = getRandomQuote();
      motivationalQuoteEl.classList.add('animate-pulse');
      
      setTimeout(() => {
        motivationalQuoteEl.classList.remove('animate-pulse');
      }, 1000);
    }

    // 获取随机鼓励语
    function getRandomQuote() {
      const randomIndex = Math.floor(Math.random() * motivationalQuotes.length);
      return motivationalQuotes[randomIndex];
    }

    // 设置提醒
    function setupReminders() {
      // 清除现有提醒
      if ('Notification' in window && Notification.permission === 'granted') {
        // 检查是否有习惯需要提醒
        const now = new Date();
        const currentHour = now.getHours();
        const currentMinute = now.getMinutes();
        
        habits.forEach(habit => {
          if (habit.reminderTime) {
            const [reminderHour, reminderMinute] = habit.reminderTime.split(':').map(Number);
            
            if (currentHour === reminderHour && currentMinute === reminderMinute) {
              // 检查今天是否已经打卡
              if (!isHabitCompletedToday(habit.id)) {
                showNotification(habit);
              }
            }
          }
        });
      }
      
      // 请求通知权限
      if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
      }
      
      // 每分钟检查一次
      setTimeout(setupReminders, 60000);
    }

    // 显示通知
    function showNotification(habit) {
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(`习惯提醒：${habit.name}`, {
          body: '是时候完成今天的打卡了！',
          icon: '/favicon.ico'
        });
      }
    }

    // 显示指定部分
    function showSection(sectionId) {
      habitDetails.classList.add('hidden');
      statsSection.classList.add('hidden');
      calendarSection.classList.add('hidden');
      achievementsSection.classList.add('hidden');
      
      document.getElementById(sectionId).classList.remove('hidden');
      
      // 如果显示日历，重新渲染
      if (sectionId === 'calendar-section') {
        renderCalendar();
      }
    }

    // 辅助函数：生成唯一ID
    function generateId() {
      return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    }

    // 辅助函数：格式化日期
    function formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }

    // 初始化应用
    document.addEventListener('DOMContentLoaded', initApp);
  </script>
</body>
</html>
