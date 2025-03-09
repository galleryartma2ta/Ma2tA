export interface Category {
    id: number;
    name: string;
    slug: string;
    description: string | null;
    parent_id: number | null;
}

export interface Artwork {
    id: number;
    title: string;
    slug: string;
    description: string;
    price: number;
    stock: number;
    image_url: string;
    category_id: number;
    artist_id: number;
    status: 'active' | 'sold' | 'hidden';
    created_at: string;
    updated_at: string;
}