(define (problem BW-rand-8)
  (:domain blocksworld)
  (:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
  (:init
    (handempty)
    (ontable b1)
    (on b2 b7)
    (on b3 b1)
    (ontable b4)
    (on b5 b3)
    (on b6 b2)
    (ontable b7)
    (on b8 b4)
    (clear b5)
    (clear b6)
    (clear b8)
  )
  (:goal
    (and
      (on b1 b5)
      (on b2 b7)
      (on b6 b1)
      (on b7 b8)
	)
  )
)


