(define (problem BW-rand-20)
  (:domain blocksworld)
  (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 - block)
  (:init
    (handempty)
    (ontable b1)
    (on b2 b4)
    (ontable b3)
    (on b4 b12)
    (on b5 b20)
    (on b6 b2)
    (on b7 b13)
    (on b8 b19)
    (on b9 b5)
    (on b10 b15)
    (on b11 b6)
    (on b12 b17)
    (on b13 b3)
    (ontable b14)
    (on b15 b1)
    (on b16 b10)
    (on b17 b16)
    (on b18 b7)
    (on b19 b18)
    (on b20 b14)
    (clear b8)
    (clear b9)
    (clear b11)
  )
  (:goal
    (and
      (on b1 b6)
      (on b2 b11)
      (on b5 b18)
      (on b8 b14)
      (on b10 b20)
      (on b11 b4)
      (on b12 b8)
      (on b13 b9)
      (on b14 b5)
      (on b15 b7)
      (on b17 b12)
      (on b18 b19)
      (on b19 b10)
      (on b20 b16)
    )
  )
)


