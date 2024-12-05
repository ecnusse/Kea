
import logging
import os
import cv2

THREGHOLD = 0.85

class Similarity(object):
    def __init__(self, sim_k) -> None:
        self.sim_k = sim_k
        self.sim_count = 0
        self.logger = logging.getLogger('SimilarityCalculator')
        

    def detected_ui_tarpit(self,input_manager):
        """
        start calculate similarity between last state screen and current screen
        """
        last_state = input_manager.policy.get_last_state()
        last_state_screen = last_state.get_state_screen()
        current_state = input_manager.device.get_current_state()
        current_state_screen = current_state.get_state_screen()
        sim_score = self.calculate_similarity(last_state_screen,current_state_screen)
        self.logger.info(f'similarity score:{sim_score}')
        if sim_score < THREGHOLD :
            self.logger.info(f'different page!')
            self.sim_count = 0
            input_manager.policy.clear_action_history()
        else:
            self.sim_count += 1   
        if self.sim_count >= self.sim_k :
            return True
        return False  
    
    @staticmethod
    def dhash(image, hash_size=8):
        resized = cv2.resize(image, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        diff = gray[:, 1:] > gray[:, :-1]

        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    @staticmethod
    def hamming_distance(hash1, hash2):
        return bin(hash1 ^ hash2).count("1")

    @staticmethod
    def calculate_similarity(fileA, fileB):
        imgA = cv2.imread(fileA)
        imgB = cv2.imread(fileB)
        hashA = Similarity.dhash(imgA)
        hashB = Similarity.dhash(imgB)
        similarity_score = 1 - Similarity.hamming_distance(hashA, hashB) / 64.0 
        return similarity_score     