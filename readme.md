### Học phần mở rộng môn Hệ điều hành
***
##### Đề bài: Giải bài toán Sudoku với multithreads, đánh giá hiệu năng trên host, docker.
1. Giải bài toán Sudoku với giải thuật Constraint Satisfaction. Không gian bài toán giống với game tree, mỗi node là 1 state.
2. Với cách hiện thực trên host và 1 container, các threads sẽ thực thi theo kiểu "depth first search", trong khi đó khi chạy chia sẽ giữa các containers, dùng *message broker*, nên thực thi theo "breath first search".