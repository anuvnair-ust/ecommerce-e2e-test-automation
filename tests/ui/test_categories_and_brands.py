import pytest

from config import settings


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "category, subcategory",
    [
        (settings.KNOWN_CATEGORY, settings.KNOWN_SUBCATEGORY),
        ("Women", "Tops"),
        ("Men", "Tshirts"),
    ],
)
def test_navigate_product_categories(page, products_page, category, subcategory):
    products_page.open_subcategory(category, subcategory)

    assert "/category_products/" in products_page.current_path()
    heading = products_page.heading_text().upper()
    assert heading == f"{category} - {subcategory} PRODUCTS".upper()
    assert products_page.product_cards.count() > 0, f"No products under {category} > {subcategory}"


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("brand", [settings.KNOWN_BRAND, "H&M", "Madame"])
def test_navigate_product_brands(page, products_page, brand):
    products_page.open_brand(brand)

    assert "/brand_products/" in products_page.current_path()
    heading = products_page.heading_text().upper()
    assert heading == f"BRAND - {brand} PRODUCTS".upper()
    assert products_page.product_cards.count() > 0, f"No products listed for brand {brand}"
