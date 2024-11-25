<template>
  <div id="chartsDiv" ref="chartsRef"></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
// import { getQuotation } from "@/request/api";
import * as echarts from "echarts";

const chartsRef = ref(null);
const option = {
  legend: {
    textStyle: {
      fontSize: 16
    },
    selected: {
      '180头': false,
    }
  },
  tooltip: {
    trigger: 'axis'
  },
  dataset: {
    source: [['']]
  },
  axisLabel: {
    color: "#7EB7FD",
    fontWeight: "500",
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    splitLine: {
      show: false
    },
  },
  yAxis: {
    type: 'value',
    splitLine: {
      show: false
    },
    name: "单位:元/Kg",
    nameLocation: 'center',
    nameGap: 30,
  },
  dataZoom: [
    {
      start: 50,
      end: 100
    },
    {
      start: 0,
      end: 10
    }
  ],
  series: Array(11).fill({ type: 'line', showSymbol: false })
};

// onMounted(() => {
//   getQuotation("1").then(res => {
//     if (res.status === 200) {
//       const product = [["product", "剪口", "10头", "20头", "30头", "40头", "60头", "80头", "120头", "180头", "无数头", "大根"]];
//       option.dataset.source = product.concat(res.data);
//       const Echarts = echarts.init(chartsRef.value);
//       Echarts.setOption(option);
//     } else {
//       console.log("获取报价失败，状态码：" + res.status);
//     }
//   }).catch(err => {
//     console.log("获取报价时发生错误：" + err);
//     console.log(err);
//   });
// });
</script>

<style scoped>
#chartsDiv {
  height: 100%;
  width: 100%;
}
</style>