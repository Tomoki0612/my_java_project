today:
	python3 scripts/today.py

next:
	@python3 scripts/next_action.py

new:
	python3 scripts/new_problem.py $(N) --ja

done:
	python3 scripts/done.py $(N)

helped:
	python3 scripts/done.py $(N) --helped

review:
	python3 scripts/review.py $(N)

.PHONY: today next new done helped review
