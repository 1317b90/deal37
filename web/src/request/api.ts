import service from "@/request/index";
import type { informationI, UserI, CommodityI, OrderI } from "@/interface";


// 获取行情
export async function getMarketTrend() {

  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const endDate = `${year}-${month}-${day}`

  return service({
    url: "https://dip.zg37.com.cn/api/portal/datasets/4/records?startDate=2022-01-01&endDate=" + endDate + "&marketId=1",
    method: "GET",
  })
}

export async function getMarketPrice(date: string) {
  //2025-03-18
  return service({
    url: "https://dip.zg37.com.cn/api/portal/daily-price/ratio?marketId=1&date=" + date,
    method: "GET",
  })
}


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



// 创建用户
export async function createUser(user: Omit<UserI, 'id'>) {
  return service({
    url: '/user',
    method: 'POST',
    data: user
  });
}

// 获取单个用户
export async function getUser(id: number) {
  return service({
    url: `/user/${id}`,
    method: 'GET'
  });
}

// 获取所有用户
export async function getAllUsers() {
  return service({
    url: '/users',
    method: 'GET'
  });
}

// 更新用户
export async function updateUser(id: number, user: Partial<UserI>) {
  console.log(user);
  return service({
    url: `/user/${id}`,
    method: 'PUT',
    data: user
  });
}

// 删除用户
export async function deleteUser(id: number) {
  return service({
    url: `/user/${id}`,
    method: 'DELETE'
  });
}

// 搜索用户
export async function searchUsers(username?: string, phone?: string) {
  return service({
    url: '/users/search',
    method: 'GET',
    params: { username, phone }
  });
}

// 根据用户名获取用户
export async function getUserByUsername(username: string) {
  return service({
    url: `/user/username/${username}`,
    method: 'GET'
  });
}

// 更新用户余额
export async function updateUserBalance(userId: number, balance: number) {
  return service({
    url: '/user/balance',
    method: 'POST',
    data: {
      user_id: userId,
      balance: balance
    }
  });
}

// 创建商品
export async function createCommodity(commodity: Omit<CommodityI, 'id'>) {
  return service({
    url: '/commodity',
    method: 'POST',
    data: commodity
  });
}

// 获取单个商品
export async function getCommodity(id: number) {
  return service({
    url: `/commodity/${id}`,
    method: 'GET'
  });
}

// 获取所有商品
export async function getAllCommodities(onShelf?: boolean) {
  const baseUrl = '/commodities';
  const url = onShelf !== undefined ? `${baseUrl}?onShelf=${onShelf}` : baseUrl;
  return service({
    url: url,
    method: 'GET'
  });
}

// 更新商品
export async function updateCommodity(id: number, commodity: Partial<CommodityI>) {
  console.log(commodity)
  return service({
    url: `/commodity/${id}`,
    method: 'PUT',
    data: commodity
  });
}

// 删除商品
export async function deleteCommodity(id: number) {
  return service({
    url: `/commodity/${id}`,
    method: 'DELETE'
  });
}

// 搜索商品
export async function searchCommodities(name?: string) {
  return service({
    url: '/commodities/search',
    method: 'GET',
    params: { name }
  });
}

// 发送消息
export async function sendMessage(message: { sender_id: number; receiver_id: number; content: string }) {
  return service({
    url: '/messages',
    method: 'POST',
    data: message
  });
}

// 获取用户的聊天记录
export async function getUserMessages(userId: number) {
  return service({
    url: `/messages/${userId}`,
    method: 'GET'
  });
}

// 获取两个用户之间的聊天记录
export async function getChatHistory(senderId: number, receiverId: number) {
  return service({
    url: `/messages/${senderId}/${receiverId}`,
    method: 'GET'
  });
}

// 获取用户的联系人列表
export async function getUserContacts(userId: number) {
  return service({
    url: `/messages/${userId}/contacts`,
    method: 'GET'
  });
}

// 获取用户的未读消息
export async function getUnreadMessages(userId: number) {
  return service({
    url: `/messages/${userId}/unread`,
    method: 'GET'
  });
}

// 标记消息为已读
export async function markMessageAsRead(messageId: number) {
  return service({
    url: `/messages/${messageId}/read`,
    method: 'PUT'
  });
}

// 创建初始消息
export async function initializeChat(senderId: number, receiverId: number) {
  return service({
    url: '/messages/init',
    method: 'POST',
    params: {
      sender_id: senderId,
      receiver_id: receiverId
    }
  });
}

// 创建支付宝订单
export async function createAlipayOrder(params: {
  buy_id: number;
  commodity_id: number;
  number: number;
  address: string;
  phone: string;
}) {
  return service({
    url: '/alipay/create',
    method: 'POST',
    data: params
  });
}


// 查询支付状态
export async function getAlipayStatus(order_id: string) {
  return service({
    url: '/alipay/status',
    method: 'GET',
    params: { order_id }
  });
}

// 获取订单列表
export async function getOrderList(params: {
  page?: number;
  limit?: number;
  sell_id?: string;
  buy_id?: string;
}) {
  return service({
    url: '/order/list',
    method: 'GET',
    params
  });
}

// 更新订单
export async function updateOrder(orderId: string, data: {
  status?: string;
  express_number?: string;
}) {
  return service({
    url: `/order/${orderId}`,
    method: 'PUT',
    data
  });
}



