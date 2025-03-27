export interface informationI {
  id?: number;
  title: string;
  content: string;
  author: string;
  img_url: string;
  created_at?: Date;
}


export interface UserI {
  id: number;
  username: string;
  password: string;
  name: string;
  phone: string;
  role: string;
  created_at?: Date;
  updated_at?: Date;
}


export interface CommodityI {
  id: number;
  name: string;        // 商品名称
  price: number;       // 商品价格
  specification: string;  // 商品规格
  inventory: number;   // 商品库存
  sales: number;       // 销量
  sell_id: number;    // 对应卖家id
  sell_name: string;  // 对应卖家名称
  image: string;      // 图片链接
  onShelf: boolean;   // 是否上架
  created_at?: Date;  // 创建时间
  updated_at?: Date;  // 更新时间
}



export const specifications = ["10头", "20头", "30头", "40头", "60头", "80头", "120头", "无数头", "统货"]

export const formatDate = (date: Date | undefined) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};