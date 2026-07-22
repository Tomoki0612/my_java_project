today:
	python3 scripts/today.py

next:
	@python3 scripts/next_action.py

new:
	python3 scripts/new_problem.py $(N)

recommend:
	python3 scripts/recommend_new.py

done:
	python3 scripts/done.py $(N)

helped:
	python3 scripts/done.py $(N) --helped

review:
	python3 scripts/review.py $(N)

doctor:
	python3 scripts/doctor.py

sync:
	python3 scripts/sync.py $(if $(M),-m "$(M)",)

test-scripts:
	python3 -m unittest discover -s scripts -p 'test_*.py'

.PHONY: today next new recommend done helped review doctor sync test-scripts
