# Coupang Price Tracker
등록해둔 쿠팡 상품의 가격을 추적하는 커스텀 컴포넌트

# Logs
2021-02-19 최초 작성

# Example
Minimal example of `configuration.yaml`
```
sensors:
- platform: coupang_price
  items:
  - product_id: 27613130
```
Complex example of `configuration.yaml`
```
sensors:
- platform: coupang_price
  items:
  - product_id: 27613130
    name: Mineral Water
    icon: mdi:bottle-tonic-outline
  - product_id: 197268194
    name: Chocolate
```
