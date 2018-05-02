package Hashing;

import java.util.ArrayList;
import java.util.LinkedList;

public class ChainedHashing extends Hashing {
    int capacity;
    ArrayList<LinkedList<Pair>> list;

    ChainedHashing(int capacity) {
        this.capacity = capacity;
        list = new ArrayList<>(capacity);
        for(int i = 0; i < capacity; i++) {
            list.add(null);
        }
    }

    private int hashing(Integer key) {
        int result = key % capacity;
        return result;
    }

    public int put(Integer key, Integer value) {
        int index = hashing(key);
        if(list.get(index) == null) {
            LinkedList<Pair> chain = new LinkedList<>();
            chain.add(new Pair(key, value));
            list.set(index, chain);
        } else {
            list.get(index).add(new Pair(key, value));
        }
        return 0;
    }

    public Integer get(Integer key) {
        int index = hashing(key);
        Integer result = null;
        if(list.get(index) != null) {
            for(Pair temp : list.get(index)) {
                if(temp.key.equals(key)) {
                    result = temp.value;
                    break;
                }
            }
        }
        return result;
    }

    public int remove(Integer key) {
        int index = hashing(key);

        int result = 0;
        if(list.get(index) != null) {
            Pair toDelete = null;
            for(Pair temp : list.get(index)) {
                if(temp.key.equals(key)) {
                    toDelete = temp;
                    break;
                }
            }
            if(toDelete != null) {
                list.get(index).remove(toDelete);
            }
        } else {
            result = -1;
        }

        return result;
    }
}