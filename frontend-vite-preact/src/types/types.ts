export interface Product {
    product_code: string;
    name: string;
    brand: string;
    url: string;
    price: number;
    scraped_nutrition: boolean;
    price_per_protein: number;
    total_protein: number;
    total_carb: number;
    price_per_carb: number;
    total_fat: number;
    price_per_fat: number;
    total_calories: number;
    price_per_calories: number;
    total_fiber: number;
    price_per_fiber: number;
    // calories: number;
    // protein: number;
    // carbs: number;
    // fat: number;
    [key: string]: any;
}