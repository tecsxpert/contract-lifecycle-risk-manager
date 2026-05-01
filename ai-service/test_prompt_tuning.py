import unittest
from prompt_tuning import PROMPT_TEMPLATES, REAL_INPUTS, score_prompt, rewrite_prompt, tune_prompts


class PromptTuningTest(unittest.TestCase):

    def test_prompt_templates_exist(self):
        self.assertTrue(PROMPT_TEMPLATES)
        self.assertTrue(REAL_INPUTS)

    def test_each_prompt_has_ten_inputs(self):
        for prompt_name, inputs in REAL_INPUTS.items():
            self.assertEqual(len(inputs), 10, f"Expected 10 inputs for {prompt_name}")

    def test_prompt_scores_are_computed(self):
        for prompt_name, template in PROMPT_TEMPLATES.items():
            inputs = REAL_INPUTS.get(prompt_name, [])
            score = score_prompt(template, inputs)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)

    def test_rewrite_prompt_generates_new_text(self):
        for template in PROMPT_TEMPLATES.values():
            rewritten = rewrite_prompt(template)
            self.assertIsInstance(rewritten, str)
            self.assertTrue(len(rewritten) > len(template))

    def test_tune_prompts_returns_scores(self):
        results = tune_prompts()
        self.assertIsInstance(results, dict)
        self.assertEqual(set(results.keys()), set(PROMPT_TEMPLATES.keys()))
        for metadata in results.values():
            self.assertIn("average_score", metadata)
            self.assertIn("needs_rewrite", metadata)
            self.assertIn("rewritten_template", metadata)


if __name__ == "__main__":
    unittest.main()
