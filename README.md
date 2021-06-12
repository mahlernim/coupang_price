# Coupang Price Tracker
A custom component for Home Assistant that tracks item prices on Coupang.com<br>
등록해둔 쿠팡 상품의 가격을 추적하는 커스텀 컴포넌트

# Logs
2021-06-12 manifest.json 필수 필드 추가<br>
2021-02-21 가격 옵션이 여러가지 있는 경우 대응<br>
2021-02-19 최초 작성

# Configuration

## Fetching product_id value
![numeric value between products/ and ?](https://raw.github.com/mahlernim/coupang_price/master/images/screenshot_fetch_product_id.png)<br>
- Copy the numeric value after `products/` in the product page url, and paste it in the yaml as `product_id`. (red box)
- If the fetched price is the price of a different quantity option, also copy the numeric value after `vendorItemId=` and paste it in the yaml as `vendor_item_id`. (blue box)
- 상품 페이지의 url에서 `products/`와 `?` 사이의 숫자 8-10자리를 복사해서 configuration.yaml에 `product_id` 값으로 지정하면 됩니다. (빨강 박스)
- 다른 수량 옵션의 가격이 인식된 경우, 추가적으로 `vendorItemId=` 뒤에 붙은 숫자 8-10 자리를 복사해서 configuration.yaml에 `vendor_item_id` 값으로 지정해줘야 합니다. (파랑 박스) 

## Yaml configuration
Minimal example of `configuration.yaml`
- 최소 설정 예시. items 아래에 리스트로 product_id 값만 넘겨주면 됩니다.
```
sensors:
- platform: coupang_price
  items:
  - product_id: 27613130
```

Complex example of `configuration.yaml`
- 모든 설정을 다 이용한 예시. 상품명 앞에 일괄적으로 붙는 접두사, 화폐 단위, 확인 주기(최소 2시간), 각 상품의 보기 편한 이름, 각 상품의 아이콘을 설정할 수 있습니다.
```
sensors:
- platform: coupang_price
  prefix: Prices
  unit_of_measurement: KRW
  scan_interval: 7200
  items:
  - product_id: 2267863198
    vendor_item_id: 71340359336
    name: Tonic Water
    icon: mdi:bottle-tonic-outline
  - product_id: 197268194
    name: Chocolate
```

# Attributes
- This custom component also fetches some useful information from the product data and saves it as attributes.
- 상품 상세 정보에서 일부 유용한 정보를 가져와 애트리뷰트 형태로 저장하게 됩니다. 자동화 등에 부가 정보가 필요할 경우 사용하시기 바랍니다.

```
price: 3900
product_id: 1232968322
vendor_item_id: 70187605147
sold_out: false
vendor: [COUPANG]
product_name: 곰곰 신선한 우유
delivery_type: ROCKET_DELIVERY
unit_price: 100ml당 195원
unit_of_measurement: 원
friendly_name: Coupang Whole Fat
icon: mdi:cup
```