(define (problem BW-rand-18)
  (:domain blocksworld)
  (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 - block)
  (:init
    (handempty)
    (on b1 b4)
    (on b2 b10)
    (on b3 b8)
    (on b4 b7)
    (on b5 b3)
    (on b6 b18)
    (on b7 b16)
    (on b8 b14)
    (on b9 b11)
    (ontable b10)
    (ontable b11)
    (ontable b12)
    (on b13 b17)
    (on b14 b2)
    (on b15 b1)
    (on b16 b13)
    (ontable b17)
    (on b18 b12)
    (clear b5)
    (clear b6)
    (clear b9)
    (clear b15)
  )
  (:goal
    (and
      (on b4 b12)
      (on b5 b15)
      (on b7 b3)
      (on b8 b1)
      (on b9 b8)
      (on b10 b17)
      (on b11 b14)
      (on b12 b13)
      (on b13 b2)
      (on b14 b5)
      (on b15 b7)
      (on b16 b10)
    )
  )
)


