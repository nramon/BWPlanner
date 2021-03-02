(define (problem BW-rand-4)
  (:domain blocksworld)
  (:objects b1 b2 b3 b4 - block)
  (:init
    (handempty)
    (on b1 b2)
    (ontable b2)
    (on b3 b4)
    (on b4 b1)
    (clear b3)
  )
  (:goal
    (and
      (on b1 b2)
      (on b3 b4)
    )
  )
)


