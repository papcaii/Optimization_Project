# Optimization_Project

maybe we can do this...

## Description

Có N đồ án tốt nghiệp 1, 2, …, N và M thầy cô cần được chia vào K hội đồng
 • Mỗi đồ án i có t(i) là giáo viên hướng dẫn
 • Giữa 2 đồ án i và j có độ tương đồng s(i,j)
 • Giữa đồ án i và giáo viên j có độ tương đồng g(i,j)
 
## Requirements

 • Số đồ án trong mỗi HĐ phải lớn hơn hoặc bằng a và nhỏ hơn hoặc bằng b
 
 • Số giáo viên trong mỗi HĐ phải lớn hơn hoặc bằng c và nhỏ hơn hoặc bằng d
 
 • Giáo viên không được ngồi hội đồng của sinh viên mình hướng dẫn
 
 • Độ tương đồng giữa các đồ án trong cùng hội đồng phải lớn hơn hoặc bằng e
 
 • Độ tương đồng giữa đồ án với giáo viên trong hội đồng phải lớn hơn hoặc bằng f
 
 • Tổng độ tương đồng giữa các đồ án và giữa đồ án với giáo viên trong các hội đồng phải lớn nhất
 
Mỗi phương án được biểu diễn bởi x(1), x(2), . . ., x(N) và y(1), y(2), . . ., y(M) trong đó x(i) là chỉ số của hội đồng mà đồ án i được phân vào, y(j) là chỉ số của hội đồng mà giáo viên j được phân vào.
Input
Dòng 1: Ghi N, M và K (1 <= N <= 1000, 1 <= M <= 200, 1 <= K <= 100)
Dòng 2: Ghi a, b, c, d, e, f
Dòng 2 + i (i = 1,…, N): ghi hàng thứ i của ma trận s
Dòng thứ N+2+i (i = 1,…, N): ghi hàng thứ i của ma trận g
Dòng cuối cùng: ghi t(1), t(2), …, t(N)

## Output

Dòng 1: ghi số nguyên dương N 
Dòng 2; ghi x(1), x(2), . . ., x(N) (các số cách nhau bởi 1 dấu cách SPACE)
Dòng 3: ghi số nguyên dương M
Dòng 4 ghi y(1) ,y(2), . . ., y(M)  (các số cách nhau bởi dấu cách SPACE)

## Example 

### Input
`
6 4 2
2 4 1 3 1 1
0 2 4 1 2 5 
2 0 5 5 3 5 
4 5 0 4 3 5 
1 5 4 0 3 2 
2 3 3 3 0 3 
5 5 5 2 3 0 
3 5 1 5 
5 2 5 3 
3 1 3 3 
5 5 1 3 
4 5 4 1 
5 3 4 5 
1 3 4 2 2 3
`
### Output
`
6
2 2 1 1 1 2
4
1 2 1 2
`
