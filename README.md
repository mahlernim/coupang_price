# Coupang Price Tracker
A custom component for Home Assistant 
등록해둔 쿠팡 상품의 가격을 추적하는 커스텀 컴포넌트

# Logs
2021-02-19 최초 작성

# Configuration

## Fetching product_id value
![numeric value between products/ and ?](https://raw.github.com/mahlernim/coupang_price/master/images/screenshot_fetch_product_id.png)<br>
- Copy the numeric value between `products/` and `?` in the product page url, and paste it in the yaml file.
- 상품 페이지의 url에서 `products/`와 `?` 사이의 숫자 8-9자리를 복사해서 configuration.yaml에 붙여넣으면 됩니다.

## Yaml configuration
Minimal example of `configuration.yaml`
- 최소 설정 예시. product_id 값만 넘겨주면 됩니다.
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
  - product_id: 27613130
    name: Mineral Water
    icon: mdi:bottle-tonic-outline
  - product_id: 197268194
    name: Chocolate
```

# Attributes
- This custom component also fetches some useful information from the product data and saves it as attributes.
- 상품 상세 정보에서 일부 유용한 정보를 가져와 애트리뷰트 형태로 저장하게 됩니다.

```
product_id: 188227098
price: 10230
sold_out: false
vendor: [COUPANG]
product_name: 코멧 아기물티슈 오리지널 캡형
delivery_type: ROCKET_DELIVERY
unit_price: 10매당 102원
unit_of_measurement: 원
friendly_name: Coupang 코멧 아기물티슈 오리지널 캡형
icon: mdi:paper-roll
```