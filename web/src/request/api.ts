import service from "@/request/index";
import type { informationI } from "@/interface";


// 获取行情
// export async function getQuotation(marketId: string) {
    
//     const now = new Date();
//     const year = now.getFullYear();
//     const month = String(now.getMonth() + 1).padStart(2, '0');
//     const day = String(now.getDate()).padStart(2, '0');
//     const endDate = `${year}-${month}-${day}`

//     return service({
//         url: "portal/datasets/4/records?startDate=2020-01-01&endDate=" + endDate + "&marketId="+marketId,
//         method: "GET",
//     })
// }

// Information 接口定义

// 创建资讯
export async function createInformation(information: Omit<informationI, 'id'>) {
  return service({
    url: "/information",
    method: "POST",
    data: information
  });
}

// 获取单个资讯
export async function getInformation(id: number) {
  return service({
    url: `/information/${id}`,
    method: "GET"
  });
}

// 获取所有资讯
export async function getAllInformation() {
  return service({
    url: "/information",
    method: "GET"
  });
}

// 更新资讯
export async function updateInformation(id: number, information: Omit<informationI, 'id'>) {
  return service({
    url: `/information/${id}`,
    method: "PUT",
    data: information
  });
}

// 删除资讯
export async function deleteInformation(id: number) {
  return service({
    url: `/information/${id}`,
    method: "DELETE"
  });
}

// 搜索资讯
export async function searchInformation(title: string) {
  return service({
    url: "/information/search",
    method: "GET",
    params: { title }
  });
}


