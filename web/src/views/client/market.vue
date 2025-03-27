<template>
  <div class="view-content">
    <div class="card-div">
      <div class="section-title">市场趋势</div>
      <div id="chartsDiv" ref="chartsRef"></div>
    </div>

    <div class="card-div">
      <div class="section-title">每日价格</div>
      <a-date-picker style="float: right; margin-top: -45px;" v-model:value="selectedDate" :format="'YYYY-MM-DD'"
        @change="handleDateChange" />
      <a-table :dataSource="tableData" :columns="columns" :loading="loading" :pagination="false">
        <template #bodyCell="{ column, record }">
          <template v-if="column.dataIndex === 'ratio'">
            <span :style="{ color: record.ratio >= 0 ? '#52c41a' : '#ff4d4f' }">
              {{ record.ratio >= 0 ? '+' : '' }}{{ record.ratio }}%
            </span>
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from "vue";
import { init } from "echarts/core";
import { LineChart, type LineSeriesOption } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent, DatasetComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import type { ComposeOption } from 'echarts/core';
import { getMarketTrend, getMarketPrice } from '@/request/api';
import dayjs from 'dayjs';

// 注册必需的组件
import { use } from "echarts/core";
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  DatasetComponent
]);

// 图表引用
const chartsRef = ref<HTMLElement | null>(null);
let chartInstance: ComposeOption<LineSeriesOption> | null = null;

// 图表配置项
const baseOption = {
  title: {
    text: '行情趋势',
    left: 'left',
    top: 0,
    textStyle: { fontSize: 16, fontWeight: 'bold' }
  },
  legend: {
    textStyle: { fontSize: 16 },
    selected: { '180头': false },
    top: 30,
  },
  tooltip: { trigger: 'axis' },
  dataset: { source: [['']] },
  axisLabel: {
    color: "#7EB7FD",
    fontWeight: "500",
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    splitLine: { show: false },
  },
  yAxis: {
    type: 'value',
    splitLine: { show: false },
    name: "单位:元/Kg",
    nameLocation: 'center',
    nameGap: 30,
  },
  dataZoom: [
    { start: 50, end: 120 },
    { start: 0, end: 10 }
  ],
  series: Array(11).fill({ type: 'line', showSymbol: false })
};

// 图例标签
const labels = [
  '剪口', '10头', '20头', '30头', '40头',
  '60头', '80头', '120头', '180头', '无数头',
  '大根', '其他'
];

// 初始化图表
const initChart = () => {
  if (!chartsRef.value) return;
  chartInstance = init(chartsRef.value) as unknown as ComposeOption<LineSeriesOption>;
  (chartInstance as any).setOption(baseOption);
};

// 更新图表数据
const updateChartData = async () => {
  try {
    const res = await getMarketTrend();
    const chartData = res.data.map((item: [string, ...number[]]) => {
      const [time, ...prices] = item;
      return [time.split(' ')[0], ...prices];
    });

    const updatedOption = {
      ...baseOption,
      legend: {
        ...baseOption.legend,
        data: labels,
        type: 'scroll',
        top: 0
      },
      dataset: { source: chartData },
      series: labels.map((label, index) => ({
        name: label,
        type: 'line',
        showSymbol: false,
        encode: { x: 0, y: index + 1 }
      }))
    };

    if (chartInstance) {
      (chartInstance as any).setOption(updatedOption);
    }
  } catch (err) {
    console.error('获取数据失败:', err);
  }
};

// 表格相关数据
const loading = ref(false);
const selectedDate = ref<dayjs.Dayjs>(dayjs());
const tableData = ref<any[]>([]);

const columns = [
  {
    title: '品种',
    dataIndex: ['specification', 'variety', 'name'],
    align: 'center',
  },
  {
    title: '规格',
    dataIndex: ['specification', 'name'],
    align: 'center',
  },
  {
    title: '今日平均价格',
    dataIndex: 'price',
    align: 'center',
    customRender: ({ text }: { text: number }) => `${text.toFixed(1)}`,
  },
  {
    title: '昨日平均价格',
    dataIndex: 'yestPrice',
    align: 'center',
    customRender: ({ text }: { text: number }) => `${text.toFixed(1)}`,
  },
  {
    title: '日涨跌',
    dataIndex: 'ratio',
    align: 'center',
  },
];

// 加载表格数据
const loadTableData = async () => {
  loading.value = true;
  try {
    const res = await getMarketPrice(selectedDate.value.format('YYYY-MM-DD'));
    tableData.value = res.data;
  } catch (err) {
    console.error('获取数据失败:', err);
  } finally {
    loading.value = false;
  }
};

// 日期变化处理
const handleDateChange = () => {
  loadTableData();
};

onMounted(() => {
  initChart();
  updateChartData();
  loadTableData();
});

onUnmounted(() => {
  if (chartInstance) {
    (chartInstance as any).dispose();
  }
});
</script>

<style scoped>
.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
}

.view-content {
  height: 100%;
  width: 100%;
  padding: 20px 150px 10px 150px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-div {

  width: 100%;
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
}

#chartsDiv {
  height: 450px;
  width: 100%;
}

.ant-table-wrapper {
  margin-top: 20px;
}
</style>